from ninja import Router
from django.http import HttpRequest, JsonResponse
from ninja.decorators import decorate_view
from django.views.decorators.cache import cache_page
import plaid
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
#from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest

from datetime import date, timedelta

from plugins.plaid import client
from plaids.models import Plaid
from plaids.schemas import ItemIDSchema, TransactionResponseSchema
from util.schemas import Token

router = Router(tags=['plaid'])

@router.post('/create_link_token')
@decorate_view(cache_page(60 * 30))
def create_link_token(request: HttpRequest):
    try:
        request_data = LinkTokenCreateRequest(
            products=[Products('transactions')],
            client_name="Penny America",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(request.user.id)
            ),
        )

    # create link token
        response = client.link_token_create(request_data)
        return JsonResponse(response.to_dict())
    except plaid.ApiException as e:
        return 500, str(e)

@router.post('/sandbox_public_token', response={200: Token})
def sandbox_public_token(request: HttpRequest, institution_id: str):
    pt_request = SandboxPublicTokenCreateRequest(
        institution_id=institution_id,
        initial_products=[Products('transactions')],
        options={'override_username': 'user_transactions_dynamic',
            'override_password': 'pass_good'}
    )
    pt_response = client.sandbox_public_token_create(pt_request)
    return Token(pt_response['public_token'])

@router.post('/gen_access_token')
def gen_access_token(request: HttpRequest, public_token: Token):
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=public_token.token
    )
    exchange_response = client.item_public_token_exchange(exchange_request)
    Plaid.objects.create(
        access_token=exchange_response['access_token'],
        item_id=exchange_response['item_id'],
        user=request.user
    )

@router.get('/institutions/{ins_id}')
def get_institution(request: HttpRequest, ins_id: str):
    request_data = InstitutionsGetByIdRequest(
        institution_id=ins_id,
        country_codes=[CountryCode('US')]
    )
    response = client.institutions_get_by_id(request_data)
    return JsonResponse(response.to_dict())

@router.get('/items', response={200: list[ItemIDSchema]})
def get_items(request: HttpRequest):
    items = request.user.plaids.all()
    return 200, items

@router.delete('/items', response={200: tuple[int, dict]})
def delete_items(request: HttpRequest, item_id: ItemIDSchema):
    response = request.user.plaids.filter(item_id=item_id.item_id).delete()
    return 200, response

@router.get('/auth')
def get_auth(request: HttpRequest):
    auths = []
    for item in request.user.plaids.all():
        access_token = item.access_token
        request_data = AuthGetRequest(access_token=access_token)
        response = client.auth_get(request_data)
        auths.append(response.to_dict())
    return JsonResponse({'auths': auths})

@router.get('/transactions', response={200: TransactionResponseSchema})
def get_transactions(request: HttpRequest):
    transactions = []
    for item in request.user.plaids.all():
        request_data = TransactionsGetRequest(
            access_token=item.access_token,
            start_date=date.today() - timedelta(days=365),
            end_date=date.today(),
        )
        response = client.transactions_get(request_data)
        item_transactions = response['transactions']
        while len(item_transactions) < response['total_transactions']:
            request_data['options'] = TransactionsGetRequestOptions(
                offset=len(transactions[item.item_id])
            )
            response = client.transactions_sync(request_data)
            item_transactions += response['transactions']
        transactions += item_transactions
    return 200, {'transactions': transactions}