from ninja import Router
from django.http import HttpRequest
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
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest

from datetime import date, timedelta

from plugins.plaid import client
from plaids.models import Plaid
from plaids.schemas import (
    ItemIDSchema,
    TransactionResponseSchema,
    LinkTokenResponseSchema,
    SPTCRequestSchema,
    InstitutionResponseSchema,
    AuthResponseSchema,
)
from util.schemas import Token, Message

router = Router(tags=['plaid'])

@router.post('/create_link_token', response={200: LinkTokenResponseSchema, frozenset({401, 404, 500}): Message})
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

        response = client.link_token_create(request_data)
        return 200, response
    except plaid.ApiException as e:
        return 500, Message(str(e))

@router.post('/sandbox_public_token', response={200: Token, frozenset({401, 404, 500}): Message})
def sandbox_public_token(request: HttpRequest, creds: SPTCRequestSchema):
    try:
        pt_request = SandboxPublicTokenCreateRequest(
            institution_id=creds.institution_id,
            initial_products=[Products('transactions')],
            options={'override_username': creds.username,
                'override_password': creds.password}
        )
        pt_response = client.sandbox_public_token_create(pt_request)
        return Token(pt_response['public_token'])
    except plaid.ApiException as e:
        return 500, Message(str(e))

@router.post('/gen_access_token', response={200: ItemIDSchema, frozenset({401, 404, 500}): Message})
def gen_access_token(request: HttpRequest, public_token: Token):
    try:
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token.token
        )
        exchange_response = client.item_public_token_exchange(exchange_request)
        Plaid.objects.create(
            access_token=exchange_response['access_token'],
            item_id=exchange_response['item_id'],
            user=request.user
        )
        return 200, exchange_response
    except plaid.ApiException as e:
        return 500, Message(str(e))

@router.get('/institutions/{ins_id}', response={200: InstitutionResponseSchema, frozenset({401, 404, 500}): Message})
def get_institution(request: HttpRequest, ins_id: str):
    try:
        request_data = InstitutionsGetByIdRequest(
            institution_id=ins_id,
            country_codes=[CountryCode('US')]
        )
        response = client.institutions_get_by_id(request_data)
        return 200, response.to_dict()
    except plaid.ApiException as e:
        return 500, Message(str(e))

@router.get('/items', response={200: list[ItemIDSchema], frozenset({401, 404}): Message})
def get_items(request: HttpRequest):
    items = request.user.plaids.all()
    return 200, items

@router.delete('/items', response={200: tuple[int, dict], frozenset({401, 404}): Message})
def delete_items(request: HttpRequest, item_id: ItemIDSchema):
    response = request.user.plaids.filter(item_id=item_id.item_id).delete()
    return 200, response

@router.get('/auth', response={200: AuthResponseSchema, frozenset({401, 404, 500}): Message})
def get_auth(request: HttpRequest):
    try:
        auths = []
        for item in request.user.plaids.all():
            access_token = item.access_token
            request_data = AuthGetRequest(access_token=access_token)
            response = client.auth_get(request_data)
            auths.append(response.to_dict())
        return 200, {'auths': auths}
    except plaid.ApiException as e:
        return 500, Message(str(e))

@router.get('/transactions', response={200: TransactionResponseSchema, frozenset({401, 404, 500}): Message})
def get_transactions(request: HttpRequest):
    try:
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
    except plaid.ApiException as e:
        return 500, Message(str(e))