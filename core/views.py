from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from .serializers import TokenExchangeSerializer


# Create your views here.
@api_view(['GET'])
def exchange_token(request):
    serializer = TokenExchangeSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


    


