import hashlib

from behavioral_patterns import ListView, CreateView, Subject, BaseSerializer, TemplateView, UpdateView
from common_utils import make_hash
from my_wsgi.templator import render
from patterns.creating_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from architect_pattern_unit_of_work import UnitOfWork

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

engine = Engine()
engine.products = []
routes = {}

@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', geo=request.get('geo', None))

@AppRoute(routes=routes, url='/history/')
class History:
    @Debug(name='History')
    def __call__(self, request):
        return '200 Ok', render('history.html')


@AppRoute(routes=routes, url='/calc/')
class Calc:
    message = {}

    def is_valid(self, data):
        print(data)
        errors = []
        err = ''
        if not data.get('kkal', None):
            err = err + f'Fill the calories; \n'
        if data.get('balt', None) == None:
            err = err + f'Fill the amount of proteins; \n'
        if data.get('fat', None) == None:
            errors.append('Fill the amount of fats')
            err = err + f'Fill the amount of fats; \n'
        if data.get('ugl', None) == None:
            err = err + f'Fill the amount of carbohydrates; \n'
        if int(data.get('balt', 0)) + int(data.get('fats', 0)) + int(data.get('carbs', 0)) != 100:
            err = err + f'Аmount of proteins, fats and carbohydrates should be 100%; \n'
        if len(engine.calc_products) == 0:
            err = err + f'Set of calculation products not filled'
        self.message['error'] =err
        return True if len(err) == 0 else False

    @Debug(name='Calc')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request.get('data', None)
            if not self.is_valid(data):
                print(f'self.is_valid(data) = {self.is_valid(data)}')
                # calculation = engine.create_calculation(data)
                return '200 Ok', render('calc.html', messages=self.message)
            else:
                return '200 Ok', render('calc.html', product_calc_list=engine.calc_products)
        else:
            return '200 Ok', render('calc.html', product_calc_list=engine.calc_products)


@AppRoute(routes=routes, url='/add_product/')
class AddProduct:
    @Debug(name='AddProduct')
    def __call__(self, request):
        if request['method'] == 'GET':
            request_params = request['request_params']
            # print(request)
            category_list = MapperRegistry.get_current_mapper('category').all()
            if request_params.get('category_id', None):
                # print(f'AddProduct. category_id = {int(request_params.get("category_id"))}')
                product_list = MapperRegistry.get_current_mapper('product').filter(category=int(request_params['category_id']))
            else:
                product_list = MapperRegistry.get_current_mapper('product').filter(category=None)
            category_id = request_params.get('category_id')
            is_admin = engine.is_admin
            return '200 Ok', render('add_product.html', category_list = category_list, product_list=product_list, category_id=category_id, is_admin = is_admin)


@AppRoute(routes=routes, url='/product_view/')
class ProductView:
    def __call__(self, request):
        print(f'ProductView = ',request['request_params'])
        request_params = request['request_params']
        product_id = int(request_params.get('product_id', None))
        product = MapperRegistry.get_current_mapper('product').find_by_id(product_id)
        category_list = MapperRegistry.get_current_mapper('category').all()
        category = MapperRegistry.get_current_mapper('category').find_by_id(product.category)
        return '200 Ok', render('product_view.html', prod=product, category_list=category_list, category=category)


@AppRoute(routes=routes, url='/product_update/')
class ProductUpdate(UpdateView):
    product_id = None
    product_name = ''

    def __call__(self, request):
        if request['method'] == 'GET':
            request_params = request['request_params']
            product_id = int(request_params.get('product_id', None))
            self.product_id = product_id
            product = MapperRegistry.get_current_mapper('product').find_by_id(product_id)
            self.product_name = product.name
            category_list = MapperRegistry.get_current_mapper('category').all()
            category = MapperRegistry.get_current_mapper('category').find_by_id(product.category)
            return '200 Ok', render('product_update.html', prod=product, category_list=category_list, category=category)
        if request['method'] == 'POST':

            data = request['data']
            self.category = data.get('category_id')
            self.category = engine.decode_value(self.category)
            category_list = MapperRegistry.get_current_mapper('category').all()

            category = None
            if self.category:
                category = MapperRegistry.get_current_mapper('category').find_id_by_name(self.category)

            self.product_id = MapperRegistry.get_current_mapper('product').find_id_by_name(self.product_name)
            product = MapperRegistry.get_current_mapper('product').find_by_id(self.product_id)
            data['product_id'] = self.product_id
            engine.update_product(product, data, category)

            product.mark_dirty()
            UnitOfWork.get_current().commit()
            product = MapperRegistry.get_current_mapper('product').find_by_id(self.product_id)
            return '200 Ok', render('product_update.html', prod=product, category_list=category_list, category=category)


class NotFoundPage:
    def __call__(self, request):
        return '404 WHAT', '404 Page not found'


@AppRoute(routes=routes, url='/contact_us/')
class ContactUs(TemplateView):
    template_name = 'contact_us.html'


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'
    template_name_post = 'add_product.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['category_list'] = MapperRegistry.get_current_mapper('category').all()
        context['product_list'] = MapperRegistry.get_current_mapper('product').all()
        context['is_admin'] = engine.is_admin
        return context

    def create_obj(self, data):
        cat_name = data['new_category_name']
        cat_name = engine.decode_value(cat_name)

        category = None
        if cat_name:
            category = MapperRegistry.get_current_mapper('category').find_by_name(cat_name)
            # category = engine.find_category_by_name(cat_name)

        if category == None:
                # or category not in engine.categories:
            new_category = engine.create_category(cat_name)
            engine.categories.append(new_category)
            new_category.mark_new()
            UnitOfWork.get_current().commit()


# контроллер - список категорий
@AppRoute(routes=routes, url='/category_list/')
class CategoryList(ListView):

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()
    # queryset = engine.categories
    template_name = 'category_list.html'


@AppRoute(routes=routes, url='/product/')
class CreateProduct(CreateView):
    template_name = 'product.html'
    template_name_post = 'add_product.html'
    category_id = None

    def get_context_data(self):
        context = super().get_context_data()
        context['category_list'] = MapperRegistry.get_current_mapper('category').all()
        context['product_list'] = MapperRegistry.get_current_mapper('product').all()
        context['category_id'] = self.category_id
        context['is_admin'] = engine.is_admin
        return context

    def create_obj(self, data):
        name = data['name']
        name = engine.decode_value(name)
        self.category_id = data.get('category_id')
        category = None

        if self.category_id:
            category = MapperRegistry.get_current_mapper('category').find_by_id(self.category_id)

        new_product = engine.create_product(data, category)
        engine.products.append(new_product)
        new_product.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/prod_list/')
class ProductsList:
    def __call__(self, request):
        if request['method'] == 'GET': # push button Calc
            request_params = request['request_params']
            if request_params.get('category_id', None):
                cat_id = request_params.get('category_id')
                cat_id = engine.decode_value(cat_id)
                if cat_id == 'все':
                    product_list = MapperRegistry.get_current_mapper('product').filter(category=None, prod_name=None)
                else:
                    product_list = MapperRegistry.get_current_mapper('product').filter(category=int(cat_id), prod_name=None)
            elif request_params.get('prod_name', None):
                prod_name =  request_params.get('prod_name')
                prod_name = engine.decode_value(prod_name)
                product_list = MapperRegistry.get_current_mapper('product').filter(category=None, prod_name=prod_name)

            is_admin = engine.is_admin

            return '200 Ok', render('product_list.html', product_list=product_list, is_admin=is_admin)


@AppRoute(routes=routes, url='/product_list/')
class AddProductCalculation:
    def __call__(self, request):
        if request['method'] == 'GET':
            request_params = request['request_params']
            product_id = request_params.get('product_id')
            product = None
            if product_id:
                product = MapperRegistry.get_current_mapper('product').find_by_id(product_id)
                # product = engine.find_product_by_id(product_id)
            if product:
                for cp in engine.calc_products:
                    # совпадение наименования и колоража - считаем что продукт уже в таблице
                    if cp.__dict__['name'] == product.__dict__['name'] and cp.__dict__['kkal'] == product.__dict__['kkal']:
                        return '200 OK', render('calc.html', product_calc_list=engine.calc_products)

                engine.calc_products.append(product)
            # print(f'calc_products = {engine.calc_products}')
            return '200 OK', render('calc.html', product_calc_list=engine.calc_products)
        if request['method'] == 'POST': # push button Calc
            data = request['data']
            calculation = engine.create_calculation(data)

            if calculation:
                engine.calculations.append(calculation)

            return '200 OK', render('calc.html', product_calc_list=engine.calc_products, calc_list = calculation.results)


@AppRoute(routes=routes, url='/admin/')
class AdminAuthentication:
    def __call__(self, request):
        if request['method'] == 'GET':
            return '200 OK', render('admin.html')
        if request ['method'] == 'POST':
            data = request['data']
            login = 'admin'
            password = data.get('password', None)
            hash = make_hash(password)
            is_correct_pswd = MapperRegistry.get_current_mapper('user').check_password(login, hash)
            if is_correct_pswd:
                engine.is_admin = True
                print(f'is_admin = {engine.is_admin}')
                messages = {}
                messages['success'] = 'authorization success'
                return '200 OK', render('calc.html', product_calc_list=engine.calc_products, messages=messages)
            else:
                engine.is_admin = False
                messages = {}
                messages['error'] = 'entered data is incorrect'
                print('Авторизация не удалась')
                return '200 OK', render('admin.html', messages=messages)


@AppRoute(routes=routes, url='/del_calc_prod/')
class DelProductCalculation:
    def __call__(self, request):
        data = request.get('request_params')
        prod = engine.find_calc_product_by_id(int(data['prod_id']))
        engine.calc_products.remove(prod)
        return '200 OK', render('calc.html', product_calc_list=engine.calc_products)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(engine.calculations).save()

