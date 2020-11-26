from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import generics
from .models import User



class UsersView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.all()
        return users