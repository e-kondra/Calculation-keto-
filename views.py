from my_wsgi.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', style=request.get('style', None))


class About:
    def __call__(self, request):
        return '200 Ok', render('about.html')


class Calc:
    def __call__(self, request):
        data = request.get('data', None)
        style = request.get('style', None)
        return '200 Ok', render('calc.html', data=data, style=style)


class AddProduct:
    def __call__(self, request):
        return '200 Ok', render('add_product.html', style=request.get('style', None))


class NotFoundPage:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact_us.html', style=request.get('style_cont', None))