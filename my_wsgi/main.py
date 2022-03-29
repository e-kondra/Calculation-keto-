"""Main application of wsgi"""


class NotFoundPage:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


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
        # rendering of pattern Front Controller
        for front in self.fronts:
            front(request)

        code, text = view(request)
        start_response(code, [('Content_Type', 'text/html')])
        return [text.encode('utf-8')]
