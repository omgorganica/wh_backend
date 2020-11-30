from django.conf.urls.static import static
from django.conf import settings
from .views import UserViewSet, OperationViewSet, ShiftViewSet, GoodsViewSet, OrderViewSet, BalanceModifierViewSet, \
    BalanceModifierHistoryViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('operations', OperationViewSet, basename='operations')
router.register('shifts', ShiftViewSet, basename='shifts')
router.register('goods', GoodsViewSet, basename='goods')
router.register('orders', OrderViewSet, basename='orders')
router.register('balance_modifier', BalanceModifierViewSet, basename='balance_modifier')
router.register('balance_modifier_history', BalanceModifierHistoryViewSet, basename='balance_modifier_history')
urlpatterns = router.urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)