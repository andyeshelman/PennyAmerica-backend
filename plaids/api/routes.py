from ninja import Router
from django.http import HttpRequest, JsonResponse
import plaid
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.auth_get_request import AuthGetRequest

from plugins.plaid import client
from plaids.models import Plaid
from util.schemas import Token

router = Router(tags=['plaid'])

@router.post('/create_link_token')
def create_link_token(request: HttpRequest):
    try:
        request_data = LinkTokenCreateRequest(
            products=[Products('transactions'), Products('auth')],
            client_name="Plaid Quickstart",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=str(request.user.id)
            )
        )

    # create link token
        response = client.link_token_create(request_data)
        return JsonResponse(response.to_dict())
    except plaid.ApiException as e:
        print(e)

# @router.post('/sandbox_public_token', response={200: Token})
# def sandbox_public_token(request: HttpRequest, institution_id: str):
#     pt_request = SandboxPublicTokenCreateRequest(
#         institution_id=institution_id,
#         initial_products=[Products('transactions')]
#     )
#     pt_response = client.sandbox_public_token_create(pt_request)
#     return Token(pt_response['public_token'])

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
    
@router.get('/auth')
def get_auth(request: HttpRequest):
    auths = []
    for item in request.user.plaids.all():
        access_token = item.access_token
        request_data = AuthGetRequest(access_token=access_token)
        response = client.auth_get(request_data)
        auths.append(response.to_dict())
    return JsonResponse({'auths': auths})

@router.get('/transactions')
def get_transactions(request: HttpRequest):
    transactions = []
    for item in request.user.plaids.all():
        access_token = item.access_token
        req = TransactionsSyncRequest(
            access_token=access_token,
        )
        response = client.transactions_sync(req)
        transactions += response['added']
        while (response['has_more']):
            req = TransactionsSyncRequest(
                access_token=access_token,
                cursor=response['next_cursor']
            )
            response = client.transactions_sync(req)
            transactions += response['added']
    return JsonResponse({'transactions': [t.to_dict() for t in transactions]})