
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (User,
                     Operation,
                     Shift_result,
                     Good,
                     Order,
                     Balance_modifier,
                     Balance_modifier_history)

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'wms_id', 'current_balance', 'image', 'is_superuser')


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('name', 'shift_goal')


class ShiftResultSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Shift_result
        fields = ('date', 'user', 'operation', 'operation_result')


class GoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shift_result
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    good = GoodSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('user', 'good')


class BalanceModifierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Balance_modifier
        fields = '__all__'


class BalanceModifierHistorySerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(many=False, read_only=True)
    assigned_by = UserSerializer(many=False, read_only=True)
    modifier = Balance_modifier(many=False, read_only=True)

    class Meta:
        model = Balance_modifier
        fields = ('assigned_to', 'assigned_by', 'modifier', 'comment')