import os

import dotenv

from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.sandbox_public_token_create_request_options import SandboxPublicTokenCreateRequestOptions
from core.utils import client



env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.load_dotenv(env_file)

def helper1():
    pt_request = SandboxPublicTokenCreateRequest(
                        institution_id="ins_1", #"ins_1"
                        initial_products=[Products('transactions')],                   
                    )

    res = client.sandbox_public_token_create(pt_request)

    public_token = res['public_token']
    return public_token




# options=SandboxPublicTokenCreateRequestOptions(
# webhook="https://"+NGROKID+".ngrok.io/webhook-transactions/")