from datetime import date


from views import Index,  Calc, AddProduct, ContactUs, CreateCategory, CategoryList, CreateProduct, \
    AddProductCalculation
#
# routes = {
#     #  '/': Index(),
#     # '/about/': About(),
#     # '/calc/': Calc(),
#     # '/add_product/': AddProduct(),
#     # '/contact_us/': ContactUs(),
#     # '/create_category/': CreateCategory(),
#     # '/category_list/': CategoryList(),
#     # '/product/': CreateProduct(),
#     # '/product_list/': AddProductCalculation()
# }

# front controller
def secret_front(request):
    request['date'] = date.today()
    # print(request['date'])

def other_front(request):
    request['key'] = 'key'

# def style_front(request):
#     with open('templates/main.css', 'r', encoding='utf-8') as f:
#         text_css = f.read()
#     request['style'] = text_css
#
# def style_cont(request):
#     with open('templates/contact_us.css', 'r', encoding='utf-8') as f:
#         text_css = f.read()
#     request['style_cont'] = text_css

# fronts = [secret_front, other_front,style_front, style_cont ]

fronts = [secret_front, other_front]


