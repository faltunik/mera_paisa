from celery import shared_task
from .utils import plaid_client



@shared_task
def get_access_token(public_token):
    """
    This taks will exchange the public_token for an access_token.
    """
    client = plaid_client()
    exchange_response = client.Item.public_token.exchange(public_token)
    return exchange_response





