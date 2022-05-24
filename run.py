import os
from wsgiref.simple_server import make_server
from wsgi_static_middleware import StaticMiddleware # класс-конструктор Middleware(тут подключаем статику)

from views import routes
from my_wsgi.main import MyFramework, DebugApplication
from front_controllers import fronts


ROOT_DIR = os.path.dirname(__name__)
STATIC_DIRS = [os.path.join(ROOT_DIR, 'staticfiles')]
# class FakeApplication(MyFramework):
#     def __init__(self, routes, fronts, settings):
#         self.application = MyFramework(routes, fronts, settings)
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

application = MyFramework(routes, fronts)
app_static = StaticMiddleware(application,
                              static_root='staticfiles',
                              static_dirs=STATIC_DIRS)

# application = DebugApplication(routes, fronts, settings)

# application = FakeApplication(routes, fronts, settings)

with make_server('', 8080, app_static) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()


