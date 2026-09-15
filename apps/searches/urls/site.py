from rest_framework.routers import SimpleRouter
from django.urls import path

from apps.catalogs.views.front import ProductViewSet
from apps.searches.views.site import Search
router = SimpleRouter()
router.register('products', ProductViewSet )

urlpatterns = [
    path('', Search.page, name='search'),
    path('search-box', Search.search_box, name='search-box'),
] + router.urls
