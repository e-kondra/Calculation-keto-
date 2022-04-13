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
        self.calculations = []

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_product(name, data):
        new_product = ProductBuilder()
        Logger.log(f'new_product= {new_product}, data = {data}')
        product_builder = DirectProductBuild()
        product_builder.constructor(new_product, data)
        return new_product.product

    def find_product_by_id(self, id):
        for product in self.products:
            if product.id == id:
                return product
        raise Exception(f'Нет продукта с id = {id}')

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

    def constructor(self, product, data):
        self._product = product
        self._product._build_mainparts(data)
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
    bzu = {}


class ProductBuilder:
    def __init__(self):
        self.product = Product()
        Logger.log(self.product)

    def _build_mainparts(self, data): # основные показатели(калорийность, вода, холестирин, наименование, категория)
        self.product.name = data['name']
        self.product.kkal = data['kkal']
        # self.product.category = data['category']
        self.product.water = data['water']
        self.product.cholesterol = data['cholesterol']


    def _build_proteins(self, data):  # белки
        proteins = data['proteins']
        dict_proteins = {}
        dict_proteins['sum_proteins'] = proteins
        self.product.bzu['proteins'] = dict_proteins

    def _build_fats(self, data):  # жиры
        fats = data['fats']
        dict_fats = {}
        dict_fats['sum_fats'] = fats
        self.product.bzu['fats'] = dict_fats

    def _build_carbs(self, data): # углеводы
        # self.carbs = data['carbs']
        pass

    def _build_vitamins(self, data): # витамины
        # self.vitA = data['vitA']
        # self.beta_carotene = data['beta_carotene']
        pass