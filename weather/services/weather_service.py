import requests
from weather.consts import *
from core.settings import API_KEY
import logging
import json
from wokengineers.helpers import CustomExceptionHandler
from wokengineers.status_code import method_not_allowed, api_call_failed
from wokengineers.consts import GET, POST

logger = logging.getLogger("django")



class WeatherAPIConfig:
    headers = {'Content-Type': 'application/json'}

    def __init__(self,):
        self.base_url = API_BASE_URL
        self.api_key = API_KEY

    def call_api(self, api_url, method, data):
        if method == GET:
            params = { 'access_key' : self.api_key}
            params.update(data)
            r = getattr(requests, method)(api_url, params=params)
            return r



class WeatherService(WeatherAPIConfig):
    methods = [GET, POST]
    
    def __validate_method(self, method):
        if method not in WeatherService.methods:
            raise CustomExceptionHandler(method_not_allowed(method))
        return method
       

    def __extracted_from_call(self, url, method, data):
        api_url = self.base_url + url
        logger.debug("api_url: %s", api_url)
        r = self.call_api(api_url=api_url, method=method, data=data)
        logger.debug("response, status: %s", r.status_code)
        logger.debug("response content : %s", r.content)
        r.raise_for_status()
        response = json.loads(r.text)
        return response, r.status_code

    def call(self, method, url, data):
        self.__validate_method(method.lower())
        try:
            return self.__extracted_from_call(
                method=method,
                url=url,
                data=data
                )   
        except requests.exceptions.RequestException as e:
            raise CustomExceptionHandler(api_call_failed(e.__str__()))

        except Exception as e:
            raise CustomExceptionHandler(api_call_failed(e.__str__()))