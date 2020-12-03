from pprint import pprint

from .serializers import UserSerializer, ShiftResultSerializer, GoodSerializer, OrderSerializer, \
    BalanceModifierSerializer, BalanceModifierHistorySerializer, FileUploaderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import User, ShiftResult, Good, Order, BalanceModifier, BalanceModifierHistory, FileUploader
from .excel_handler import handle_excel
from django.conf import settings
import os


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
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
        serializer = FileUploaderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            filename = os.path.split(serializer.data['file'])[1]
            results = handle_excel(os.path.join(settings.BASE_DIR, 'media\\files', filename))

            for item in results:
                try:
                    user = User.objects.get(wms_id=item['Pers No'])
                    ShiftResult.objects.create(
                        date=item['DATE'],
                        user=user,
                        picking=item['Boxes Picked Picking'],
                        transportations=item['Overall Transports'],
                        loading=item['Loadings'],
                    )
                except Exception as e:
                    print(e)
            return Response(serializer.data)


class BalanceModifierViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceModifierSerializer
    queryset = BalanceModifier.objects.all()


class BalanceModifierHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceModifierHistorySerializer
    queryset = BalanceModifierHistory.objects.all()
