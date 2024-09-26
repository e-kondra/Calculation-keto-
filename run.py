from my_wsgi.main import MyFramework, DebugApplication
from urls import fronts
from wsgiref.simple_server import make_server
from views import routes
from wsgiref.util import setup_testing_defaults



# class FakeApplication(MyFramework):
#     def __init__(self, routes, fronts):
#         self.application = MyFramework(routes, fronts)
#         super().__init__(routes,fronts)
#
#     @staticmethod
#     def fake_view():
#         return '200 OK', [b'Hello from Fake']
#
#     def __call__(self, env, start_response):
#         # setup_testing_defaults(env)
#         path = env['PATH_INFO']
#         print(f'path = {path}')
#         code, body  = self.fake_view()
#         start_response(code, [('Content-Type', 'text/html')])
#         return body

# application = MyFramework(routes, fronts)

application = DebugApplication(routes, fronts)

# application = FakeApplication(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()


