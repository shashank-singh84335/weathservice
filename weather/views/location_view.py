from rest_framework import viewsets
from weather.serializers import LocationRequestSerializer
from weather.models import LocationDetail
from wokengineers.helpers.custom_mixins import *
from wokengineers.consts import STATUS_ACTIVE

class LocationViewSet(viewsets.GenericViewSet, CustomCreateModelMixin, CustomListModelMixin, CustomRetrieveModelMixin,
                  CustomDestroyModelMixin):
    queryset = LocationDetail.objects.filter(status=STATUS_ACTIVE).all()
    serializer_class = LocationRequestSerializer

