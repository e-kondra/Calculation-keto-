from abc import ABCMeta, abstractmethod


class Requests(metaclass=ABCMeta):
    @staticmethod
    def parse_input_data(data: str):
        """converting a string into a dict"""
        # str like '127.0.0.1:8080?id=1&category=10'
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @abstractmethod
    def get_request_params(self, environ):
        pass

class GetRequest(Requests):
    dict_value = 'request_params'

    def get_request_params(self, environ):
        str = environ['QUERY_STRING']
        get_params = GetRequest.parse_input_data(str)
        return get_params


class PostRequest(Requests):
    dict_value = 'data'
    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        length_data = environ.get('CONTENT_LENGTH')
        content_length = int(length_data) if length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result_dict = {}
        if data:
            str = data.decode(encoding='utf-8')
            result_dict = self.parse_input_data(str)
        return result_dict

    def get_request_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data


class GetRequestClass():
    req = {
        'POST': PostRequest(),
        'GET': GetRequest(),
    }
