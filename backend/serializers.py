from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework.relations import PrimaryKeyRelatedField
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
        fields = ('id', 'first_name', 'last_name', 'email', 'wms_id', 'current_balance', 'image', 'is_superuser')


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('id', 'name', 'shift_goal')


class ShiftResultSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    operation_name = serializers.CharField(source='operation.name')

    class Meta:
        model = Shift_result
        fields = ('id', 'date', 'user', 'first_name', 'last_name', 'operation', 'operation_name', 'operation_result')


class GoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Good
        fields = ('id', 'name', 'price', 'image')


class OrderSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all())
    good = PrimaryKeyRelatedField(queryset=Good.objects.all())
    # user = UserSerializer()
    # good = GoodSerializer()

    class Meta:
        model = Order
        fields = ('id', 'user', 'good')

    def validate(self,validated_data):
        if validated_data['user'].current_balance < validated_data['good'].price:
            raise serializers.ValidationError(f"You haven\'t got enough balance for this action." \
            f"Your current balance is {validated_data['user'].current_balance}")
        return validated_data

    def create(self, validated_data):
        User = validated_data['user']
        Order_data = Order.objects.create(
            user=validated_data['user'],
            good=validated_data['good'],
        )
        Order_data.save()

        User.current_balance = User.current_balance - validated_data['good'].price
        User.save()

        return Order_data

class BalanceModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance_modifier
        fields = '__all__'


class BalanceModifierHistorySerializer(serializers.ModelSerializer):
    assigned_to = PrimaryKeyRelatedField(queryset=User.objects.all())
    assigned_by = PrimaryKeyRelatedField(queryset=User.objects.all())
    modifier = PrimaryKeyRelatedField(queryset=Balance_modifier.objects.all())

    class Meta:
        model = Balance_modifier_history
        fields = ('id', 'assigned_to', 'assigned_by', 'modifier', 'comment')
        depth = 1

    def create(self, validated_data):
        assigned_user = validated_data['assigned_to']
        balance_modifier_history = Balance_modifier_history.objects.create(
            assigned_to=validated_data['assigned_to'],
            assigned_by=validated_data['assigned_by'],
            modifier=validated_data['modifier'],
            comment=validated_data.get('comment', '')
        )
        balance_modifier_history.save()

        assigned_user.current_balance = assigned_user.current_balance + validated_data['modifier'].delta
        assigned_user.save()

        return balance_modifier_history
