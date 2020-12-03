from .serializers import UserSerializer, ShiftResultSerializer, GoodSerializer, OrderSerializer, \
    BalanceModifierSerializer, BalanceModifierHistorySerializer, FileUploaderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import User, Shift_result, Good, Order, Balance_modifier, Balance_modifier_history, FileUploader
from .excel_handler import handle_excel
from django.conf import settings
import os


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftResultSerializer
    queryset = Shift_result.objects.all()


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
            try:
                # handle_excel(serializer.data['file']) # '../media/files/test.xlsx'
                handle_excel(os.path.join(settings.BASE_DIR2, serializer.data['file'])) # '../media/files/test.xlsx'
            except Exception as e:
                print(e)
            return Response(serializer.data)


class BalanceModifierViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceModifierSerializer
    queryset = Balance_modifier.objects.all()


class BalanceModifierHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceModifierHistorySerializer
    queryset = Balance_modifier_history.objects.all()
