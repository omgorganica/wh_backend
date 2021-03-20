from django.conf.urls.static import static
from django.conf import settings

from .views import UserViewSet, ShiftsViewSet, GoodsViewSet, OrderViewSet, BalanceModifierViewSet, \
    BalanceModifierHistoryViewSet, FileUploaderViewSet, ShiftsAvgView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('shifts', ShiftsViewSet, basename='shifts')
router.register('goods', GoodsViewSet, basename='goods')
router.register('orders', OrderViewSet, basename='orders')
router.register('balance_modifier', BalanceModifierViewSet, basename='balance_modifier')
router.register('balance_modifier_history', BalanceModifierHistoryViewSet, basename='balance_modifier_history')
router.register('file_uploader', FileUploaderViewSet, basename='file_uploader')
router.register('mean_stat', ShiftsAvgView, basename='mean_stat')
urlpatterns = router.urls

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


