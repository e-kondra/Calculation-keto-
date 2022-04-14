import abc
import quopri



class Category:
    auto_id = 0
    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category

class Engine:
    def __init__(self):
        self.categories = []
        self.products = []
        self.calc_products = []
        self.calculations = []

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'Нет категории с id = {id}')

    # @staticmethod
    def create_product(self, data, category):
        new_product = ProductBuilder()
        # Logger.log(f'new_product= {new_product},new_product.product.name = {new_product.product.name}, new_product.product.proteins = {new_product.product.proteins}')
        product_builder = DirectProductBuild()
        product_builder.constructor(new_product, data, category)
        return new_product.product

    def find_product_by_id(self, id):
        for product in self.products:
            if product.id == int(id):
                return product
        raise Exception(f'Нет продукта с id = {id}')

    def create_calculation(self, data):
        return None


    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('LOG. ', text)


class DirectProductBuild:
    def __init__(self):
        self._product = None

    def constructor(self, product, data, category):
        self._product = product
        self._product._build_mainparts(data, category)
        self._product._build_proteins(data)
        self._product._build_fats(data)
        self._product._build_carbs(data)
        self._product._build_vitamins(data)


class Product:
    name = ''
    category = None
    kkal = 0
    water = 0
    cholesterol = 0
    proteins = {}
    fats = {}
    carbs = {}
    vitamins = {}


class ProductBuilder:
    auto_id = 0
    def __init__(self):
        self.product = Product()
        self.product.id = ProductBuilder.auto_id
        ProductBuilder.auto_id += 1
        self.product.proteins = {}
        self.product.fats = {}
        self.product.carbs = {}
        self.product.vitamins = {}

    def _build_mainparts(self, data, category): # основные показатели(калорийность, вода, холестирин, наименование, категория)
        self.product.name = Engine.decode_value(data['name'])
        self.product.kkal = data['kkal']
        self.product.category = category
        self.product.water = data['water']
        self.product.cholesterol = data['cholesterol']

    def _build_proteins(self, data):  # белки
        self.product.proteins['proteins'] = data['proteins']

    def _build_fats(self, data):  # жиры
        self.product.fats['fats'] = data['fats']

    def _build_carbs(self, data): # углеводы
        self.product.carbs['carbs'] = data['carbs']

    def _build_vitamins(self, data): # витамины
        self.product.vitamins['vitA'] = data['vitA']
        self.product.vitamins['beta_carotene'] = data['beta_carotene']


class Calculation:
    def __init__(self, ):
        self.energy = 0
        self.bzu = {}
        self.products = []
