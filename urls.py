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

def style_front(request):
    with open('templates/main.css', 'r', encoding='utf-8') as f:
        text_css = f.read()
    request['style'] = text_css

fronts = [secret_front, other_front, style_front]


