from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from .serializers import (
                    TokenExchangeSerializer,  GetTransactionsSerializer, 
                    GetAccountSerializer,  TransactionUpdateSerializer)

import os


# Create your views here.

# api to exchange token
@api_view(['POST'])
def exchange_token(request):
    print("we have recieved the request for exchange of token")
    print("plaid client id: ", os.environ['PLAID_CLIENT_ID'], "palid secret: ", os.environ['PLAID_SECRET'], "plaid env: ", os.environ['PLAID_ENV'])
    serializer = TokenExchangeSerializer(data=request.data)
    print("serializer is", serializer)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# api to get transaction details
@api_view(['GET'])
def get_transactions_details(request):
    serializer = GetTransactionsSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# api to get account details
@api_view(['GET'])
def get_account_details(request):
    serializer = GetAccountSerializer(data = request.data)
    if serializer.is_valid(raise_exception= True):
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#api to update transactions
@api_view(['POST'])
def update_transaction(request):
    serializer = TransactionUpdateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)







        
    


