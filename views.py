from my_wsgi.templator import render
from patterns.creating_patterns import Engine, Logger


engine = Engine()
engine.categories.append(engine.create_category('мясо'))
engine.categories.append(engine.create_category('рыба'))

print(engine.categories)

class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class About:
    def __call__(self, request):
        return '200 Ok', render('about.html')


class Calc:
    def __call__(self, request):
        data = request.get('data', None)
        # style = request.get('style', None)
        return '200 Ok', render('calc.html', data=data)


class AddProduct:
    def __call__(self, request):
        return '200 Ok', render('add_product.html', category_list = engine.categories)


class NotFoundPage:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


class ContactUs:
    def __call__(self, request):
        # return '200 OK', render('contact_us.html', style=request.get('style_cont', None))
        return '200 OK', render('contact_us.html')

class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            # Logger.log(f"request[data] = {request['data']}")
            print(data)
            cat_name = data['name']
            cat_name = engine.decode_value(cat_name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = engine.find_category_by_id(int(category_id))

            new_category = engine.create_category(cat_name, category)

            engine.categories.append(new_category)
            return '200 OK', render('add_product.html', category_list = engine.categories)
        else:
            categories = engine.categories
            return '200 OK', render('create_category.html', category_list = categories)

# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        Logger.log('Список категорий')
        return '200 OK', render('category_list.html', category_list=engine.categories)

class CreateProduct:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = engine.decode_value(name)

            new_product = engine.create_product(name, data)

            engine.products.append(new_product)
            print(engine.products)
            Logger.log('Создаем новый продукт')
            return '200 OK', render('product.html')
        else:
            Logger.log('GET Создаем новый продукт')
            return '200 OK', render('product.html')