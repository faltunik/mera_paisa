from datetime import datetime, date
import json

from celery import shared_task
import plaid
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest

from .manager import task_lock
from .utils import client







@shared_task(bind=True)
def get_access_token(self, public_token):
    """
    This taks will exchange the public_token for an access_token.
    """
    taskid = self.request.id
    with task_lock("task-lock", taskid , lock_expire_seconds=10) as acquired:
        if acquired:
            try: 
                exchange_request = ItemPublicTokenExchangeRequest(
                 public_token=public_token
                )
                print("exchange request is", exchange_request)
                exchange_response = client.item_public_token_exchange(exchange_request)
                exchange_response =  json.dumps(exchange_response.to_dict())
                access_token = exchange_response['access_token']
                return access_token

            except plaid.ApiException as e:
                print("Unable to get exchange token : {}".format(e))
                return None

@shared_task(bind=True)
def get_transactions(self, access_token, start_date, end_date):
    
    taskid = self.request.id
    with task_lock("task-lock", taskid , lock_expire_seconds=10) as acquired:
        if acquired:
            try:
                txn_request = TransactionsGetRequest(
                    access_token=access_token,
                    start_date=start_date,
                    end_date=end_date,
                )
                txn_response = client.transactions_get(txn_request)
                return txn_response

            except plaid.ApiException as e:
                print("Unable to get transactions: {}".format(e))
                return None
            

@shared_task(bind=True)
def get_accounts(self, access_token):
    taskid = self.request.id
    with task_lock("task-lock", taskid , lock_expire_seconds=10) as acquired:
        if acquired:
            request = AccountsGetRequest(access_token=access_token)
            response = client.accounts_get(request)
            return response



# celery -A txn  worker -l info -P gevent
# watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A txn  worker -l info -P gevent
#celery worker --app=worker.app --pool=gevent





