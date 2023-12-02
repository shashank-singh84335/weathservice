from rest_framework import viewsets
from weather.serializers import LocationRequestSerializer
from rest_framework.response import Response
from weather.models import LocationDetail
from wokengineers.helpers.custom_mixins import CustomRetrieveModelMixin, get_object, get_response
from wokengineers.consts import STATUS_ACTIVE, GET
from weather.services import WeatherService
from weather.consts import *
from wokengineers.status_code import success
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from wokengineers.helpers import CustomExceptionHandler
from wokengineers.status_code import field_required_error
from weather.status_code import Statuses
from datetime import datetime
from django.core.cache import cache
from weather.status_code import api_call_failed_weahter

class WeatherViewSet(viewsets.GenericViewSet, CustomRetrieveModelMixin):
    queryset = LocationDetail.objects.filter(status=STATUS_ACTIVE).all()
    serializer_class = LocationRequestSerializer
    throttle_scope = 'weather_api_throttle'

    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        cache_key = f'weather_data_{id}'
        response = cache.get(cache_key)
        if not response:
            location_object = get_object(self)
            payload = { 
                "query" : location_object.name
            }
            response, _ = WeatherService().call(GET, CURRENT_DATA_URL, data=payload)
            if response.get("success") == False:
                raise CustomExceptionHandler(api_call_failed_weahter(response))
            response = get_response(success, response)
            cache.set(cache_key, response, 600) # 10 min cache   

        return Response(response)
    

class WeatherHistoryViewSet(viewsets.GenericViewSet, CustomRetrieveModelMixin):
    queryset = LocationDetail.objects.filter(status=STATUS_ACTIVE).all()
    serializer_class = LocationRequestSerializer
    throttle_scope = 'weather_api_throttle'

    def __validate_date_string(self, date_string):
        date_list = date_string.split(';')
        date_format = '%Y-%m-%d'
        for date_str in date_list:
            try:
                datetime.strptime(date_str, date_format)
            except ValueError:
                raise CustomExceptionHandler(Statuses.invalid_date)
        return date_string

    skip_param = openapi.Parameter('historical_date', openapi.IN_QUERY,
                                    description="Example: 2015-01-21 for a single date or 2015-01-21;2015-01-22 for multiple dates '%Y-%m-%d' ", 
                                    type=openapi.TYPE_STRING, required=True)
    # @method_decorator(cache_page(60 * 15))    
    @swagger_auto_schema(manual_parameters=[skip_param])
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        historical_date = request.query_params.get("historical_date")
        if not historical_date:
            raise CustomExceptionHandler(field_required_error("historical_date"))

        cache_key = f'weather_data_{id}_{historical_date}'
        response = cache.get(cache_key)
        if not response:
            location_object = get_object(self)
            historical_date = self.__validate_date_string(historical_date)
            payload = { 
                "query" : location_object.name,
                "historical_date" : historical_date
            }
            response, _  = WeatherService().call(GET, HISTORICAL_DATA_URL, data=payload)
            if response.get("success") == False:
                raise CustomExceptionHandler(api_call_failed_weahter(response))
            response = get_response(success, response)
            cache.set(cache_key, response, 600) # 10 min cache   

        return Response(response)