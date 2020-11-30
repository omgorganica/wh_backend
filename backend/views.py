from .serializers import UserSerializer, OperationSerializer, ShiftResultSerializer, GoodSerializer, OrderSerializer, \
    BalanceModifierSerializer, BalanceModifierHistorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Operation, Shift_result, Good, Order, Balance_modifier, Balance_modifier_history


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class OperationViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()


class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftResultSerializer
    queryset = Shift_result.objects.all()


class GoodsViewSet(viewsets.ModelViewSet):
    serializer_class = GoodSerializer
    queryset = Good.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    # def list(self, request):
    #     queryset = Order.objects.all()
    #     serializer = OrderSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request):
    #     serializer = OrderSerializer
    #     if request.user.current_balance < request.good.price:
    #         return Response(serializer.data)

class BalanceModifierViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceModifierSerializer
    queryset = Balance_modifier.objects.all()


class BalanceModifierHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceModifierHistorySerializer
    queryset = Balance_modifier_history.objects.all()

    # def create(self, request, *args, **kwargs):
    #     try:
    #         data = request.pop('modifier')
    #         balance_modifier = Balance_modifier_history.objects.create(**data)
    #
    #         assigned_user = User.objects.filter(pk=request.data.get('assigned_to')['id'])
    #         updated_balance = assigned_user.current_balance + request.data.get('delta')
    #         assigned_user.update(current_balance=updated_balance)
    #
    #         return Response(balance_modifier, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         print(e)

