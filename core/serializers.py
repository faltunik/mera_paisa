from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

import plaid

from .models import Item
from .tasks import get_access_token, get_transactions, get_accounts



class TokenExchangeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    public_token = serializers.CharField()
    item_id = serializers.CharField(required=False, read_only=True)
    access_token = serializers.CharField(required=False, read_only=True)
    request_id = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        username = None
        public_token = None
        try:
            username = data.get('username')
            public_token = data.get('public_token')
            if not username or not public_token:
                raise ValidationError('Invalid Credentials for Token Exchange')
        except Exception as e:
            raise ValidationError(str(e))

        item = None
        try: 
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.') 

        try:
            item = Item.objects.filter(user__username=username).first()
            print("item is: ", item)
            if item:
                raise ValidationError('Access token already generated')
        except ObjectDoesNotExist:
            raise ValidationError('Invalid user username')

        exchange_response = {}

        try:
            print("We will start the background task to get executed")
            exchange_response = get_access_token.delay(public_token)
            access_token_response = exchange_response.get()
            #item.access_token = exchange_response['access_token']
            item.access_token = access_token_response.get()
            if item.access_token:
                item.save()
            else:
                raise ValidationError('Unable to get access token')
        except Exception as e:
            raise ValidationError(str(e))
        exchange_response['username'] = username
        exchange_response['public_token'] = public_token
        return exchange_response

    class Meta:
        model = Item
        fields = (
            'username',
            'public_token',
            'item_id',
            'request_id',
            'access_token',
        )


class GetTransactionsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    start_date = serializers.DateField(format="%Y-%m-%d")
    end_date = serializers.DateField(format="%Y-%m-%d")
    transactions = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)
        try:
            if not username:
                raise ValidationError('Invalid Credentials')
            if not start_date:
                raise ValidationError('Start Date not provided')
            if not end_date:
                raise ValidationError('End date not provided')
        except Exception as e:
            raise ValidationError(str(e))

        start_date = "{:%Y-%m-%d}".format(start_date)
        end_date = "{:%Y-%m-%d}".format(end_date)
        item = None
        try: 
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.') 

        try:
            item = Item.objects.filter(user__username=username).first()
            if not item.access_token:
                raise ValidationError('Access Token not generated')

        except Exception as e:
            raise ValidationError(str(e))

        access_token = item.access_token
        output = {}
        transactions = {}

        try:
            transactions = get_transactions.delay(
                access_token, start_date, end_date)
            transactions = transactions.get()
        except plaid.errors.PlaidError as e:
            raise ValidationError(str(e))
        output['username'] = username
        output['start_date'] = start_date
        output['end_date'] = end_date
        output['transactions'] = transactions.get('transactions')
        return output

    class Meta:
        model = User
        fields = (
            'username',
            'start_date',
            'end_date',
            'transactions',
        )


class GetAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    accounts = serializers.JSONField(required=False, read_only=True)
    item = serializers.JSONField(required=False, read_only=True)
    numbers = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        try:
            if not username:
                raise ValidationError('Invalid Credentials')
        except Exception as e:
            raise ValidationError(str(e))

        item = None

        try:
            item = Item.objects.filter(user__username=username).first()
            if not item.access_token:
                raise ValidationError('Access Token not generated')
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist.')

        access_token = item.access_token
        accounts = {}

        try:
            accounts = get_accounts.delay(access_token)
            accounts = accounts.get()
        except plaid.errors.PlaidError as e:
            raise ValidationError(str(e))
        accounts['username'] = username
        return accounts

    class Meta:
        model = User
        fields = (
            'username',
            'accounts',
            'item',
            'numbers'
        )

class TransactionUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    transaction_id = serializers.CharField()
    transaction = serializers.JSONField(required=False, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        transaction_id = data.get('transaction_id', None)
        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise ValidationError('User Does not exist')
        
        try :
            Item = Item.objects.filter(user__username=username).first()
        except ObjectDoesNotExist:
            raise ValidationError('Item Does not exist')

        access_token = user.access_token
        transaction = {}
        try:
            start_date = '{:%Y-%m-%d}'.format(datetime.now() + timedelta(-30))
            end_date = '{:%Y-%m-%d}'.format(datetime.now())
            transactions = get_transactions.delay(
                access_token, start_date, end_date)
            transactions = transactions.get()
            transactions = transactions['transactions']
            transaction = next(
                filter(lambda x: x.get('transaction_id') == transaction_id, transactions))
            if not transaction:
                raise ValidationError('Invalid Transaction')
        except plaid.errors.PlaidError as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise ValidationError(str(e))

        data = {}
        data['username'] = username
        data['transaction_id'] = transaction_id
        data['transaction'] = transaction
        return data

    class Meta:
        model = Item
        fields = (
            'username',
            'transaction_id',
            'transaction'
        )
