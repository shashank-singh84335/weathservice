from rest_framework import serializers
from weather.models import LocationDetail
from weather.status_code import Statuses
from wokengineers.serializers.fields import CustomCharField
from wokengineers.helpers import CustomExceptionHandler
from wokengineers.consts import STATUS_ACTIVE

def is_valid_latlong(latitude, lower_range, upper_range):
    try:
        latitude = float(latitude)
        return lower_range <= latitude <= upper_range
    except ValueError:
        return False

class LocationRequestSerializer(serializers.ModelSerializer):
    name = CustomCharField(required=True)
    latitude = CustomCharField(required=True)
    longitude = CustomCharField(required=True)

    def validate_latitude(self, value):
        if not is_valid_latlong(value, -80, 80):
            raise CustomExceptionHandler(Statuses.invalid_latitude)
        return value

    def validate_longitude(self, value):
        if not is_valid_latlong(value, -180, 180):
            raise CustomExceptionHandler(Statuses.invalid_longitude)
        return value
    
    def validate(self, attrs):
        location_detail_obj = LocationDetail.objects.filter(**attrs, status=STATUS_ACTIVE)
        if location_detail_obj.exists():
            raise CustomExceptionHandler(Statuses.location_exists)
        return super().validate(attrs)
    
    class Meta:
        model = LocationDetail
        fields = ['id', 'name', 'latitude', 'longitude']