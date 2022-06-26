from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Item
from .tasks import get_access_token



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
            item = Item.objects.get(user__username=username)
            if item.access_token:
                raise ValidationError('Access token already generated')
        except ObjectDoesNotExist:
            raise ValidationError('Invalid user username')

        exchange_response = {}

        try:
            exchange_response = get_access_token.delay(public_token)
            exchange_response = exchange_response.get()
            item.access_token = exchange_response['access_token']
            item.save()
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