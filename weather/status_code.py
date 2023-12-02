

class Statuses:
    
    invalid_latitude = {"status_code": 1000100, "message" : "Invalid latitude"}
    invalid_longitude = {"status_code": 1000101, "message" : "Invalid longitude"}
    location_exists = {"status_code": 1000102, "message" : "Location already exists"}
    invalid_date = {"status_code": 1000103, "message" : "Date format not supported"}


def api_call_failed_weahter(data):
    return {'status_code': 1000104, 'message': f"api call failed {data}",}