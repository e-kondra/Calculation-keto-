"""Main application of wsgi"""
import quopri
from pprint import pprint

from wsgi_requests import GetRequest, PostRequest



class NotFoundPage:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'

class DebugLog:
    def __call__(self, function):
        def wrapper(*args, **kwargs):
            method = args[1]['REQUEST_METHOD']
            if method == 'GET':
                parameters = GetRequest().get_request_params(args[1])
            elif method == 'POST':
                parameters =  PostRequest().get_request_params(args[1])
            print(f"method = {method}, parameters = {parameters}")
            res = function(*args, **kwargs)
            return res
        return wrapper


class MyFramework:
    """Main Framework's callable class"""
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts


    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        # necessarily add closing tag
        if path in self.routes:
            view = self.routes[path]
        else:
            view = NotFoundPage()

        request = {}
        #
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = data
            # print(f'POST-запрос: {MyFramework.decode_value(data)}')
        if method == 'GET':
            parameters = GetRequest().get_request_params(environ)
            request['request_params'] = parameters
        # print(request)
        # rendering of pattern Front Controller
        for front in self.fronts:
            front(request)

        code, text = view(request)
        start_response(code, [('Content_Type', 'text/html')])
        return [text.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


# logging wsgi-application + decorator(just for homework)
class DebugApplication(MyFramework):

    def __init__(self, routes, fronts):
        self.application = MyFramework(routes, fronts)
        super().__init__(routes, fronts)

    @DebugLog()
    def __call__(self, env, start_response):
        return self.application(env, start_response)

