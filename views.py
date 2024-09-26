from my_wsgi.templator import render
from patterns.creating_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

engine = Engine()
engine.categories.append(engine.create_category('мясо'))
engine.categories.append(engine.create_category('рыба'))
engine.categories.append(engine.create_category('молочные продукты'))
engine.products = []
cat2 = engine.find_category_by_id(2)
cat0 = engine.find_category_by_id(0)
cheese = engine.create_product({'name': 'сыр Чеддер', 'kkal': 404, 'proteins':22.9, 'fats': 33.31,
                                              'carbs': 3.1, 'water': '', 'cholesterol':'', 'vitA':'', 'beta_carotene':'', }, cat2)
engine.products.append(cheese)
liver = engine.create_product({'name': 'говяжья печень', 'kkal': 134, 'category_id':'0', 'proteins':21.39, 'fats': 1.23,
                                              'carbs': 0, 'water': '', 'cholesterol':'','vitA':'', 'beta_carotene':'',}, cat0)
engine.products.append(liver)
pig_liver = engine.create_product({'name': 'свиная печень', 'kkal': 134, 'category_id':'0', 'proteins':21.34, 'fats': 3.7,
                                              'carbs': 0, 'water': '', 'cholesterol':'','vitA':'', 'beta_carotene':'',}, cat0)
engine.products.append(pig_liver)

routes = {}

@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html')

@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 Ok', render('about.html')

@AppRoute(routes=routes, url='/calc/')
class Calc:
    @Debug(name='Calc')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request.get('data', None)
            calculation = engine.create_calculation(data)
            return '200 Ok', render('calc.html', product_list=engine.products)
        else:
            return '200 Ok', render('calc.html', product_list=engine.products)


@AppRoute(routes=routes, url='/add_product/')
class AddProduct:
    @Debug(name='AddProduct')
    def __call__(self, request):
        request_params = request['request_params']
        category_id = request_params.get('category_id')
        return '200 Ok', render('add_product.html', category_list = engine.categories, product_list=engine.products, category_id=category_id)


class NotFoundPage:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


@AppRoute(routes=routes, url='/contact_us/')
class ContactUs:
    def __call__(self, request):
        return '200 OK', render('contact_us.html')


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            print(data)
            cat_name = data['name']
            cat_name = engine.decode_value(cat_name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = engine.find_category_by_id(int(category_id))

            if category not in engine.categories:
                new_category = engine.create_category(cat_name, category)
                engine.categories.append(new_category)

            return '200 OK', render('add_product.html', category_list = engine.categories, product_list=engine.products )
        else:
            categories = engine.categories
            return '200 OK', render('create_category.html', category_list = categories, product_list=engine.products)

# контроллер - список категорий
@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        return '200 OK', render('category_list.html', category_list=engine.categories)


@AppRoute(routes=routes, url='/product/')
class CreateProduct:
    @Debug(name='CreateProduct')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = engine.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = engine.find_category_by_id(int(category_id))

            new_product = engine.create_product(data, category)
            Logger.log(f'new_product = {data}')
            engine.products.append(new_product)

            return '200 OK', render('add_product.html', category_list = engine.categories, product_list=engine.products)
        else:
            request_params = request['request_params']
            category_id = request_params.get('category_id')
            return '200 OK', render('product.html', category_list = engine.categories, category_id = category_id)


@AppRoute(routes=routes, url='/product_list/')
class AddProductCalculation():
    @Debug(name='AddProductCalculation')
    def __call__(self, request):
        if request['method'] == 'GET':
            request_params = request['request_params']
            product_id = request_params.get('product_id')
            product = None
            if product_id:
                product = engine.find_product_by_id(product_id)

            if product and product not in engine.calc_products:
                engine.calc_products.append(product)

            return '200 OK', render('calc.html', product_calc_list=engine.calc_products)
        if request['method'] == 'POST': # push button Calc
            data = request['data']
            calculation = engine.create_calculation(data)

            if calculation:
                engine.calculations.append(calculation)

            return '200 OK', render('calc.html', product_calc_list=engine.calc_products, calc_list = calculation.results)