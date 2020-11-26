from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import UserRegistrationView,UserLoginView,UsersView


urlpatterns = [
    path('users/', UsersView.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)