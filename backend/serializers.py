from django.db.models import Avg
from rest_framework_jwt.settings import api_settings
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import (User,
					 Shift,
					 Good,
					 Order,
					 BalanceModifier,
					 BalanceModifierHistory,
					 FileUploader)

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
		'id', 'first_name', 'last_name', 'email', 'wms_id', 'current_balance', 'image', 'is_superuser', 'is_staff',
		'is_active')
		ref_name = 'UserSerializer'


class ShiftsResultSerializer(serializers.ModelSerializer):
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')

	class Meta:
		model = Shift
		fields = ('id', 'date', 'user', 'first_name', 'last_name', 'transportations', 'picking', 'loading','result')


class GoodSerializer(serializers.ModelSerializer):
	class Meta:
		model = Good
		fields = ('id', 'name', 'price', 'image')


class OrderSerializer(serializers.ModelSerializer):

	class Meta:
		model = Order
		fields = ('id', 'user', 'good', 'status','created')

	def validate(self, validated_data):
		if validated_data['user'].current_balance < validated_data['good'].price:
			raise ValidationError(f"You haven\'t got enough balance for this action." \
								  f"Your current balance is {validated_data['user'].current_balance}")
		return validated_data

	def to_representation(self, obj):
		self.fields['user'] = UserSerializer()
		self.fields['good'] = GoodSerializer()
		return super(OrderSerializer, self).to_representation(obj)

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
		model = BalanceModifier
		fields = '__all__'


class BalanceModifierHistorySerializer(serializers.ModelSerializer):
	assigned_to = UserSerializer()
	assigned_by = UserSerializer()
	modifier = BalanceModifierSerializer()

	class Meta:
		model = BalanceModifierHistory
		fields = ('id', 'assigned_to', 'assigned_by', 'modifier', 'comment', 'created')
		depth = 1

	'''
    Из POST запроса берем данные для изменения баланса assigned_to юзера на основании значения modifier.delta
    '''

	def create(self, validated_data):
		assigned_user = validated_data['assigned_to']
		balance_modifier_history = BalanceModifierHistory.objects.create(
			assigned_to=validated_data.get['assigned_to'],
			assigned_by=validated_data.get('assigned_by', None),
			modifier=validated_data['modifier'],
			comment=validated_data.get('comment', '')
		)
		balance_modifier_history.save()
		assigned_user.current_balance = assigned_user.current_balance + validated_data['modifier'].delta
		assigned_user.save(update_fields=['current_balance'])
		return balance_modifier_history


class FileUploaderSerializer(serializers.ModelSerializer):
	class Meta:
		model = FileUploader
		fields = ('file', 'upload_date')

	def validate(self, data):
		'''
        Проверка на расширение файла
        '''
		extension = data['file'].name.split('.')[1]
		allowed_extensions = ['xls', 'xlsx']
		if extension not in allowed_extensions:
			raise ValidationError(f"File extension *.{extension} is not allowed. Please use {allowed_extensions}")
		return data


class CustomUserSerializer(DjoserUserSerializer):
	class Meta(DjoserUserSerializer.Meta):
		fields = (
		'id', 'first_name', 'last_name', 'email', 'wms_id', 'current_balance', 'image', 'is_superuser', 'is_staff',
		'is_active')


class MeanStatSeralizer(serializers.ModelSerializer):
	picking_avg = serializers.SerializerMethodField()
	transportations_avg = serializers.SerializerMethodField()
	loading_avg = serializers.SerializerMethodField()
	result_avg = serializers.SerializerMethodField()

	class Meta:
		model = Shift
		fields = ('picking_avg','transportations_avg','loading_avg','result_avg','id')

	def get_picking_avg(self, obj):
		avg = Shift.objects.filter(picking__gt=0).aggregate(Avg('picking'))
		return avg

	def get_transportations_avg(self, obj):
		avg = Shift.objects.filter(transportations__gt=0).aggregate(Avg('transportations'))
		return avg

	def get_loading_avg(self, obj):
		avg = Shift.objects.filter(loading__gt=0).aggregate(Avg('loading'))
		return avg

	def get_result_avg(self, obj):
		avg = Shift.objects.filter(result__gt=0).aggregate(Avg('result'))
		return avg

