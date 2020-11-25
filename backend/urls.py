from django.urls import path
from .views import UserViewSet
from django.conf.urls.static import static
from django.conf import settings
from .views import UserRegistrationView


urlpatterns = [
    path('register', UserRegistrationView.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)