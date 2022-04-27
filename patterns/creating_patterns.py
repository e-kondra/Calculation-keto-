import abc
import quopri
import copy
import sqlite3
from datetime import date

from architect_pattern_unit_of_work import DomainObject
from behavioral_patterns import Subject, DBWriter


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name

class Admin(User, Subject):
    def __init__(self, name):
        super().__init__(name)

class OrdinaryUser(User, Subject):
    def __init__(self, name):
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'admin': Admin,
        'o_user': OrdinaryUser
    }
    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category(DomainObject):
    auto_id = 0
    def __init__(self, name):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name



class Engine:
    def __init__(self):
        self.categories = []
        self.products = []
        self.calc_products = []
        self.calculations = []
        self.o_users = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    def get_o_user(self, name) -> OrdinaryUser:
        for item in self.o_users:
            if item.name == name:
                return item

    @staticmethod
    def create_category(name, category=None):
        return Category(name,)

    def find_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
        raise Exception(f'Нет категории с id = {id}')

    def find_category_by_name(self, name):
        for category in self.categories:
            if category.name == name:
                return category
        return None

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
        new_calculation = CalculationBuilder()
        calc_builder = DirectCalculationBuild()
        calc_builder.constructor(new_calculation, data, self.calc_products)
        self.calc_products = []
        return new_calculation.calc

    def find_calculation_by_id(self, id):
        for calc in self.calculations:
            if calc.id == int(id):
                return calc
        raise Exception(f'Нет расчета с id = {id}')

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

# Use pattern Prototype
class CalculationPrototype:
    def clone(self):
        return copy.deepcopy(self)


class Calculation(CalculationPrototype):
    def __init__(self, kkal=0, bzu=None, products=None, results=None):
        self.date_calc = None
        self.kkal = kkal
        self.bzu = bzu if bzu else {}
        self.products = products if products else []
        self.results = results if results else {}

# Use pattern Builder
class DirectCalculationBuild:
    def __init__(self):
        self._calc = None

    def constructor(self, calc, data, prod_list):
        self._calc = calc
        self._calc._build_mainparts(data)
        self._calc._build_products(prod_list)
        self._calc._build_results(data)


class CalculationBuilder(Subject):
    auto_id = 0

    def __init__(self):
        self.calc = Calculation()
        self.calc.id = CalculationBuilder.auto_id
        CalculationBuilder.auto_id += 1
        self.calc.bzu = {}
        self.calc.products = []
        self.calc.results = []
        self.observers = []
        self.attach(DBWriter())

    def _build_mainparts(self, data):
        self.calc.date_calc = date.today()
        self.calc.kkal = int(data.get('kkal'))
        # todo. Добавить проверку на сумму б/ж/у = 100% и заполненность полей
        self.calc.bzu['balt'] = float(data.get('balt'))
        self.calc.bzu['fat'] = float(data.get('fat'))
        self.calc.bzu['ugl'] = float(data.get('ugl'))

    def _build_products(self, prod_list):
        # todo. Добавить проверку на количество/качество введенных продуктов
        self.calc.products = copy.deepcopy(prod_list)


    def _build_results(self, data):
        x = self.calc.kkal / len(self.calc.products)
        for prod in self.calc.products:
            print(prod.id, prod.name)
            result = {}
            result['product_id'] = prod.id
            result['name'] = prod.name
            m = x/prod.kkal
            result['kkal'] = round(float(prod.kkal) * m,1)
            result['proteins'] = round(float(prod.proteins['proteins'])* m, 3)
            result['fats'] = round(float(prod.fats['fats'] * m),3)
            result['carbs'] = round(float(prod.carbs['carbs'] * m),3)
            result['weight'] = round(100 * m, 1)

            self.calc.results.append(result)
        sum_kkal = 0
        sum_proteins = 0
        sum_fats = 0
        sum_carbs = 0
        sum_weight = 0
        for res in self.calc.results:
            sum_kkal += res['kkal']
            sum_proteins += res['proteins']
            sum_fats += res['fats']
            sum_carbs += res['carbs']
            sum_weight += res['weight']

        sum_result = {}
        sum_result['name'] = 'ИТОГО: '
        sum_result['kkal'] = round(sum_kkal,1)
        sum_result['proteins'] = round(sum_proteins, 3)
        sum_result['fats'] = round(sum_fats, 3)
        sum_result['carbs'] = round(sum_carbs, 3)
        sum_result['weight'] = round(sum_weight, 1)
        self.calc.results.append(sum_result)
        self.notify()


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

class Product(DomainObject):
    id = None
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
        self.product.category = None
        self.product.proteins = {}
        self.product.fats = {}
        self.product.carbs = {}
        self.product.vitamins = {}

    def _build_mainparts(self, data, category): # основные показатели(калорийность, вода, холестирин, наименование, категория)
        print(f'category_build_mainparts = {category}')
        self.product.id = int(data.get('id'))
        self.product.name = Engine.decode_value(data['name'])
        self.product.kkal = int(data.get('kkal'))
        self.product.category = category
        self.product.water = data.get('water')


    def _build_proteins(self, data):  # белки
        self.product.proteins['proteins'] = float(data.get('proteins'))

    def _build_fats(self, data):  # жиры
        self.product.fats['fats'] = float(data.get('fats'))

    def _build_carbs(self, data): # углеводы
        self.product.carbs['carbs'] = float(data.get('carbs'))

    def _build_vitamins(self, data): # витамины
        self.product.vitamins['vitA'] = data.get('vitA')
        self.product.vitamins['beta_carotene'] = data.get('beta_carotene')

class ItemMapper:
    classes = {
        'categories': Category,
        'products': Product,
        'calculation': Calculation
    }

    def __init__(self, connection, tablename):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = tablename
        self.column_list = self.get_column_list()

    def get_column_list(self):
        for row in self.connection.execute(f"pragma table_info('{self.tablename}')").fetchall():
            self.column_list.append(row[1])

    def get_cursor_tuple(self, obj):
        if obj.cursor_tuple:
            return obj.cursor_tuple
        else:
            variables = obj.__dict__
            cursor_list = []
            for item in self.column_list[1:]:
                cursor_list.append(variables.get(item, None))
            cursor_tuple = tuple(cursor_list)
            return cursor_tuple

    def insert(self, obj):
        # формируем список колонок в таблице
        column_str = str(self.column_list[1:])
        column_str = column_str.replace("'", "").replace('[', '(').replace(']', ')')
        # список из вопросов
        questions_str = '?,' * len(self.column_list[1:])
        questions_str = questions_str[:-1]

        cursor_tuple = self.get_cursor_tuple(obj)

        statement = f'INSERT INTO {self.tablename} {column_str} VALUES ({questions_str})'
        self.cursor.execute(statement, cursor_tuple)

        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            category = Category(name)
            category.id = id
            result.append(category)
        return result

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(result[1])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_id_by_name(self, name):
        statement = f'SELECT id FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (name,))
        return self.cursor.fetchone()[0]

    def find_by_name(self, name):
        statement = f'SELECT id, name FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        if result:
            return Category(result[1])
        else:
            return None

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('calc.db')

class ProductMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'product'

    def all(self):
        statement = f'SELECT * FROM {self.tablename} WHERE is_active = 1'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, category_id, name, is_active, kkal, water, proteins, fats, carbs = item
            print(item)
            product = Product()
            product.id = id
            product.category = category_id
            product.name = name
            product.kkal = kkal
            product.water = water
            product.proteins = {}
            product.proteins['proteins'] = proteins
            product.fats = {}
            product.fats['fats'] = fats
            product.carbs = {}
            product.carbs['carbs'] = carbs
            result.append(product)
        print(f'result = {result}')
        return result

    def insert(self, obj):
        proteins = float(obj.proteins.get("proteins", 0))
        fats = float(obj.fats.get("fats", 0))
        carbs = float(obj.carbs.get("carbs",0))
        category_id = MapperRegistry.get_current_mapper('category').find_id_by_name(obj.category.name)

        statement = f"INSERT INTO {self.tablename} (category_id, name, is_active, kkal, water, proteins, fats, carbs) VALUES (?,?,?,?,?,?,?,?)"
        self.cursor.execute(statement, (category_id, obj.name, 1, obj.kkal, obj.water, proteins, fats, carbs))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def find_by_id(self, id):
        statement = f'SELECT id, category_id, name, kkal, water, proteins, fats, carbs FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        id, category_id, name, kkal, water, proteins, fats, carbs = result
        data = {'id': id, 'name': name, 'kkal': kkal, 'water': water, 'proteins': proteins, 'fats': fats, 'carbs': carbs}
        category = category_id
        print(name, proteins)
        new_product = ProductBuilder()
        # Logger.log(f'new_product= {new_product},new_product.product.name = {new_product.product.name}, new_product.product.proteins = {new_product.product.proteins}')
        product_builder = DirectProductBuild()
        product_builder.constructor(new_product, data, category)

        print(result)
        if result:
            return new_product.product
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'product': ProductMapper,
        'category': CategoryMapper,
    }

    @staticmethod
    def get_mapper(object):

        if isinstance(object, Category):
            return CategoryMapper(connection)
        if isinstance(object, Product):
            return ProductMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')