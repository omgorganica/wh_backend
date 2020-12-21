from django.db.models import F
from .serializers import UserSerializer, ShiftResultSerializer, GoodSerializer, OrderSerializer, \
	BalanceModifierSerializer, BalanceModifierHistorySerializer, FileUploaderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import User, ShiftResult, Good, Order, BalanceModifier, BalanceModifierHistory, FileUploader
from .excel_handler import handle_excel
from django.conf import settings
import os
import logging


class UserViewSet(viewsets.ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()


class ShiftViewSet(viewsets.ViewSet):
	serializer_class = ShiftResultSerializer
	queryset = ShiftResult.objects.all()


class GoodsViewSet(viewsets.ModelViewSet):
	serializer_class = GoodSerializer
	queryset = Good.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
	serializer_class = OrderSerializer
	queryset = Order.objects.all()


class FileUploaderViewSet(viewsets.ModelViewSet):
	serializer_class = FileUploaderSerializer
	queryset = FileUploader.objects.all()

	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			filename = os.path.split(serializer.data['file'])[1]
			try:
				results = handle_excel(os.path.join(settings.BASE_DIR, 'media\\files',
													filename))  # Список словарей, содержащих итоги смены каждого сотрудника
				balance_modifier = BalanceModifier.objects.get(
					for_shift_result=True)  # Единственный модификатор, использующийся автоматически для итогов смены
				superuser = User.objects.filter(
					is_superuser=True).first()  # Не принципиально какой superuser будет числится в assigned_by У BalanceModifierHistory
				for item in results:

					picking = item['Boxes Picked Picking'] / settings.WORK_GOAL['picking']
					shifting = item['Overall Transports'] / settings.WORK_GOAL['shifting']
					loading = item['Loadings'] / settings.WORK_GOAL['loadings']
					result = round((picking + shifting + loading), 1)
					user = User.objects.get(wms_id=item['Pers No'])

					'''
					Если суммарная производительность по 3 операциям сотрудника за смену больше 1,
					то создается новый модификатор баланса, добавляющий ему на счет виртуальную валюту.
					Модификатор увеличивается пропорционально результату смены
					'''
					if result > 1 and not ShiftResult.objects.get(date=item['DATE'], user=user):
						user.current_balance = F('current_balance') + balance_modifier.delta * result
						user.save(update_fields=['current_balance'])

						BalanceModifierHistory.objects.create(
							assigned_by=superuser,
							assigned_to=user,
							modifier=balance_modifier,
							comment='Автоматическое пополнение по итогам смены'
						)

						'''
						Создание результата смены для каждого сотрудника. Если смена уже есть- обновить данные
						'''

						ShiftResult.objects.update_or_create(date=item['DATE'], user=user, defaults={
							'picking': item['Boxes Picked Picking'],
							'transportations': item['Overall Transports'],
							'loading': item['Loadings'], 'result': result})

					else:
						logging.error(f'User {user} for date {item["DATE"]} was already uploaded')
			except Exception as e:
				logging.error(e)

		return Response(serializer.data)


class BalanceModifierViewSet(viewsets.ModelViewSet):
	serializer_class = BalanceModifierSerializer
	queryset = BalanceModifier.objects.all()


class BalanceModifierHistoryViewSet(viewsets.ModelViewSet):
	serializer_class = BalanceModifierHistorySerializer
	queryset = BalanceModifierHistory.objects.all()

	def create(self, request):
		serializer = FileUploaderSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
