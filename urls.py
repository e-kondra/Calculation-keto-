from datetime import date

from views import Index, About, Calc, AddProduct

routes = {
    '/': Index(),
    '/about/': About(),
    '/calc/': Calc(),
    '/add_product/': AddProduct(),
}


# front controller
def secret_front(request):
    request['data'] = date.today()
    print(request['data'])

def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]


