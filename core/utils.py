import os
import plaid
from plaid.api import plaid_api
from dotenv import load_dotenv


configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': os.environ['PLAID_CLIENT_ID'],
        'secret': os.environ['PLAID_SECRET'],
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)












