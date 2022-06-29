from django.urls import path
from .import views


urlpatterns = [
    path('exchangetoken/', views.exchange_token, name='exchange_token'),
    path('gettransactions/', views.get_transactions_details, name= 'transactions_details'),
    path('getaccounts/', views.get_account_details, name= 'account_details'),
    path('updatetransactions/', views.update_transaction, name= 'update_transaction'),

]