import plaid
from plaid.api import plaid_api
import os

configuration = plaid.Configuration(
    host=getattr(plaid.Environment, os.getenv('PLAID_ENV', 'Sandbox')),
    api_key={
        'clientId': os.getenv('PLAID_CLIENT_ID'),
        'secret': os.getenv('PLAID_SECRET'),
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)