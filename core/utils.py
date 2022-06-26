import os
from plaid import Client

# os.environ
def plaid_client():
    return Client(
        client_id= os.environ['PLAID_CLIENT_ID'],
        secret=os.environ['PLAID_SECRET'],
        environment=os.environ['PLAID_ENV']
    )
