import time

# structural pattern Decorator
class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


# structural pattern Decorator
class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def decor_time(method):
            def timed(*args, **kwargs):
                tb = time.time()
                res = method(*args, **kwargs)
                te = time.time()
                delta = te - tb

                print(f'Debug. {self.name} время выполнения {delta:2.2f} ms')
                return res
            return timed
        return decor_time(cls)