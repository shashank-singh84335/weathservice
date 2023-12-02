from django.urls import path
from weather.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'location', LocationViewSet, basename='location')
router.register(r'weather/location', WeatherViewSet, basename='weather/location')
router.register(r'history', WeatherHistoryViewSet, basename='history')
urlpatterns = router.urls

urlpatterns += [
    # path("weather/location", WeatherViewSet.as_view(), name='weather'),
    # path("type", EventTypeView.as_view(), name='event_type'),
    # path("user", EventUserView.as_view(), name='event_type'),
]
