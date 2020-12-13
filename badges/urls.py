from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as yasg_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),

]

urlpatterns += yasg_urls