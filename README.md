# weathservice

There is crud api for location

I am wheatherstack for fetching current weather based on location name

I have throttling on endpoints caching is also implemented on these two endpoints
    weather/v1/weather/location/{id}/
    weather/v1/history/{id}/?historical_date={historical_date}

One endpoint works "weather/v1/weather/location/{id}/" other one doesn't because it requires subscription for the api

'weather_api_throttle': '500/minute',
'weather_api_cache' : 10 min ttl for both api's with different keys


using Redis for caching backend and throttling


STEPS TO RUN SERVER:

DOWNLOAD DOCKER ON YOUR MACHINE

1. docker-compose up --build


