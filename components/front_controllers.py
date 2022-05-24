from json import  loads
from requests import get
from datetime import date

# геолокация (на index.html пример вывода)
def get_geo_info(environ, request):
    ip_addr = environ.get('REMOTE_ADDR', '')
    ip_addr = '91.108.35.134' # for test in localhost
    if ip_addr:
        request_url = 'https://geolocation-db.com/jsonp/' + ip_addr
        response = get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        request['geo'] = loads(result)


def secret_front(environ, request):
    request['date'] = date.today()
    # print(request['date'])


fronts = [secret_front, get_geo_info]