from rest_framework.routers import SimpleRouter

from apps.catalogs.views.front import CategoryViewSet, ProductLastOfferApiView, ProductViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet )
router.register('last-offer', ProductLastOfferApiView )
# router.register('product-last-offer', LastOfferAPIView )
urlpatterns = [] + router.urls