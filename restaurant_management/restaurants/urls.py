""""restaurant app urls"""
from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import RestaurantMenuViewSet, RestaurantMenuAPIView,\
    GetWinnerRestaurantView

router = DefaultRouter()
router.register(r'menus', RestaurantMenuViewSet, basename='restaurant-menu')
urlpatterns = router.urls
urlpatterns += [path('restaurant-menus/', RestaurantMenuAPIView.as_view(),
                    name="restaurants"),
                path('winning-restaurant/', GetWinnerRestaurantView.as_view(),
                    name="winning-restaurant")]
