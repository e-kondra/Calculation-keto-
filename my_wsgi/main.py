"""Main application of wsgi"""
import ntpath
import quopri
from os import path
from pprint import pprint

from wsgi_requests import GetRequest, PostRequest
from components.content_types import CONTENT_TYPES_MAP



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
    def __init__(self, routes, fronts, settings):
        self.routes = routes
        self.fronts = fronts
        self.settings = settings


    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        # necessarily add closing tag
        if not path.endswith('/'):
            path = f'{path}/'
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

        if path in self.routes:
            view = self.routes[path]
            content_type = self.get_content_type(path)
            code, text = view(request)
            text = text.encode('utf-8')
        # static in context!
        elif path.startswith(self.settings.STATIC_URL):
            print(self.settings.STATIC_URL)
            # /static/images/logo.jpg/ -> images/logo.jpg
            file_path = path[len(self.settings.STATIC_URL): len(path)-1]
            content_type = self.get_content_type(file_path)
            code, text = self.get_static(self.settings.STATIC_FILES_DIR, file_path)

        else:
            view = NotFoundPage()
            content_type = self.get_content_type(path)
            code, text = view(request)
            text = text.encode('utf-8')

        for front in self.fronts:
            front(request)

        start_response(code, [('Content_Type', content_type)])
        return [text]

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower()
        extension = path.splitext(file_name)[1]
        return content_types_map.get(extension, "text/html")
        pass

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content

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

    def __init__(self, routes, fronts, settings):
        self.application = MyFramework(routes, fronts, settings)
        super().__init__(routes, fronts, settings)

    @DebugLog()
    def __call__(self, env, start_response):
        return self.application(env, start_response)

