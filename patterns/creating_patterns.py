import abc
import hashlib
import quopri
import copy
import sqlite3
from datetime import date

from architect_pattern_unit_of_work import DomainObject
from behavioral_patterns import Subject, DBWriter


# абстрактный пользователь
class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password


class Admin(User, Subject):
    def __init__(self, name, password):
        super().__init__(name, password)
        self.is_admin = True


class OrdinaryUser(User, Subject):
    def __init__(self, name, password):
        super().__init__(name, password)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'admin': Admin,
        'o_user': OrdinaryUser
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, password):
        return cls.types[type_](name, password)


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
        self.is_admin = False

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    def get_o_user(self, name) -> OrdinaryUser:
        for item in self.o_users:
            if item.name == name:
                return item

    @staticmethod
    def create_category(name, category=None):
        return Category(name, )

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

    def update_product(self, product, data, category):
        upd_product = ProductUpdater(product)
        # print(f'upd_product = {upd_product}')
        product_builder = DirectProductBuild()
        product_builder.updater(upd_product, data, category)
        # print(upd_product.product.name, upd_product.product.kkal)
        # return upd_product.product

    # @staticmethod
    def create_product(self, data, category):
        new_product = ProductBuilder()
        # Logger.log(f'new_product= {new_product},new_product.product.name = {new_product.product.name}, new_product.product.proteins = {new_product.product.proteins}')
        product_builder = DirectProductBuild()
        product_builder.constructor(new_product, data, category)
        return new_product.product

    def find_calc_product_by_id(self, id):
        for product in self.calc_products:
            if product.id == int(id):
                return product
        raise Exception(f'Нет продукта с id = {id}')

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
            # print(prod.id, prod.name)
            result = {}
            result['product_id'] = prod.id
            result['name'] = prod.name
            m = x / prod.kkal
            result['kkal'] = round(float(prod.kkal) * m, 1)
            result['proteins'] = round(float(prod.proteins['proteins']) * m, 3)
            result['fats'] = round(float(prod.fats['fats'] * m), 3)
            result['carbs'] = round(float(prod.carbs['carbs'] * m), 3)
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
        sum_result['kkal'] = round(sum_kkal, 1)
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
        self._product._build_microelements(data)

    def updater(self, product, data, category):
        self._product = product
        self._product._build_mainparts(data, category)
        self._product._build_proteins(data)
        self._product._build_fats(data)
        self._product._build_carbs(data)
        self._product._build_vitamins(data)
        self._product._build_microelements(data)



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
        self.product.product_id = None
        self.product.category = None
        self.product.proteins = {}
        self.product.fats = {}
        self.product.carbs = {}
        self.product.vitamins = {}
        self.product.microelements = {}

    def _build_mainparts(self, data, category):  # основные показатели(калорийность, вода, наименование, категория)
        # print(f'category_build_mainparts = {category}')
        # self.product.id = int(data.get('id'))
        self.product.name = Engine.decode_value(data['name'])
        if data.get('product_id', None):
            self.product.product_id = int(data.get('product_id', None))
        self.product.kkal = int(data.get('kkal'))
        self.product.category = category
        self.product.water = self.get_float(data, 'water')
        self.product.ash = self.get_float(data, 'ash')

    def get_float(self, data, name):
        return float(data.get(name, None)) if data.get(name, None) else None

    def _build_proteins(self, data):  # белки
        self.product.proteins['proteins'] = float(data.get('proteins'))
        self.product.proteins['tryptophan'] = self.get_float(data, 'tryptophan')
        self.product.proteins['threonine'] = self.get_float(data, 'threonine')
        self.product.proteins['isoleucine'] = self.get_float(data, 'isoleucine')
        self.product.proteins['leucine'] = self.get_float(data, 'leucine')
        self.product.proteins['lysine'] = self.get_float(data, 'lysine')
        self.product.proteins['methionine'] = self.get_float(data, 'methionine')
        self.product.proteins['cystine'] = self.get_float(data, 'cystine')
        self.product.proteins['phenylalanine'] = self.get_float(data, 'phenylalanine')
        self.product.proteins['tyrosine'] = self.get_float(data, 'tyrosine')
        self.product.proteins['valine'] = self.get_float(data, 'valine')
        self.product.proteins['arginine'] = self.get_float(data, 'arginine')
        self.product.proteins['histidine'] = self.get_float(data, 'histidine')
        self.product.proteins['alanine'] = self.get_float(data, 'alanine')
        self.product.proteins['aspartic'] = self.get_float(data, 'aspartic')
        self.product.proteins['glutamic'] = self.get_float(data, 'glutamic')
        self.product.proteins['glycine'] = self.get_float(data, 'glycine')
        self.product.proteins['proline'] = self.get_float(data, 'proline')
        self.product.proteins['serine'] = self.get_float(data, 'serine')

    def _build_fats(self, data):  # жиры
        self.product.fats['fats'] = float(data.get('fats'))
        self.product.fats['saturated'] = self.get_float(data, 'saturated')
        self.product.fats['butyric'] = self.get_float(data, 'butyric')
        self.product.fats['caproic'] = self.get_float(data, 'caproic')
        self.product.fats['caprylic'] = self.get_float(data, 'caprylic')
        self.product.fats['capric'] = self.get_float(data, 'capric')
        self.product.fats['lauric'] = self.get_float(data, 'lauric')
        self.product.fats['myristic'] = self.get_float(data, 'myristic')
        self.product.fats['palmitic'] = self.get_float(data, 'palmitic')
        self.product.fats['stearic'] = self.get_float(data, 'stearic')
        self.product.fats['arachinoic'] = self.get_float(data, 'arachinoic')
        self.product.fats['behenic'] = self.get_float(data, 'behenic')
        self.product.fats['lignoceric'] = self.get_float(data, 'lignoceric')
        self.product.fats['monounsaturated'] = self.get_float(data, 'monounsaturated')
        self.product.fats['palmitoleic'] = self.get_float(data, 'palmitoleic')
        self.product.fats['oleic'] = self.get_float(data, 'oleic')
        self.product.fats['gadolin'] = self.get_float(data, 'gadolin')
        self.product.fats['erucic'] = self.get_float(data, 'erucic')
        self.product.fats['nervonic'] = self.get_float(data, 'nervonic')
        self.product.fats['polyunsaturated'] = self.get_float(data, 'polyunsaturated')
        self.product.fats['linoleic'] = self.get_float(data, 'linoleic')
        self.product.fats['linolenic'] = self.get_float(data, 'linolenic')
        self.product.fats['alpha_linolenic'] = self.get_float(data, 'alpha_linolenic')
        self.product.fats['gamma_linolenic'] = self.get_float(data, 'gamma_linolenic')
        self.product.fats['eicosadiene'] = self.get_float(data, 'eicosadiene')
        self.product.fats['arachidonic'] = self.get_float(data, 'arachidonic')
        self.product.fats['eicosapentaenoic'] = self.get_float(data, 'eicosapentaenoic')
        self.product.fats['docosapentaenoic'] = self.get_float(data, 'docosapentaenoic')
        self.product.fats['sterol'] = self.get_float(data, 'sterol')
        self.product.fats['cholesterol'] = self.get_float(data, 'cholesterol')
        self.product.fats['phytosterols'] = self.get_float(data, 'phytosterols')
        self.product.fats['stigmasterol'] = self.get_float(data, 'stigmasterol')
        self.product.fats['campesterol'] = self.get_float(data, 'campesterol')
        self.product.fats['beta_sitosterol'] = self.get_float(data, 'beta_sitosterol')
        self.product.fats['trans'] = self.get_float(data, 'trans')
        self.product.fats['mono_trans'] = self.get_float(data, 'mono_trans')
        self.product.fats['poly_trans'] = self.get_float(data, 'poly_trans')

    def _build_carbs(self, data):  # углеводы
        self.product.carbs['carbs'] = float(data.get('carbs'))
        self.product.carbs['glucose'] = self.get_float(data, 'glucose')
        self.product.carbs['fructose'] = self.get_float(data, 'fructose')
        self.product.carbs['galactose'] = self.get_float(data, 'galactose')
        self.product.carbs['sucrose'] = self.get_float(data, 'sucrose')
        self.product.carbs['lactose'] = self.get_float(data, 'lactose')
        self.product.carbs['maltose'] = self.get_float(data, 'maltose')
        self.product.carbs['sum_sugar'] = self.get_float(data, 'sum_sugar')
        self.product.carbs['fiber'] = self.get_float(data, 'fiber')
        self.product.carbs['starch'] = self.get_float(data, 'starch')

    def _build_vitamins(self, data):  # витамины
        self.product.vitamins['vitA'] = self.get_float(data, 'vitA')
        self.product.vitamins['beta_carotene'] = self.get_float(data, 'beta_carotene')
        self.product.vitamins['alpha_carotene'] = self.get_float(data, 'alpha_carotene')
        self.product.vitamins['vitD'] = self.get_float(data, 'vitD')
        self.product.vitamins['vitD2'] = self.get_float(data, 'vitD2')
        self.product.vitamins['vitD3'] = self.get_float(data, 'vitD3')
        self.product.vitamins['vitE'] = self.get_float(data, 'vitE')
        self.product.vitamins['vitC'] = self.get_float(data, 'vitC')
        self.product.vitamins['vitB1'] = self.get_float(data, 'vitB1')
        self.product.vitamins['vitB2'] = self.get_float(data, 'vitB2')
        self.product.vitamins['vitB3'] = self.get_float(data, 'vitB3')
        self.product.vitamins['vitB4'] = self.get_float(data, 'vitB4')
        self.product.vitamins['vitB5'] = self.get_float(data, 'vitB5')
        self.product.vitamins['vitB6'] = self.get_float(data, 'vitB6')
        self.product.vitamins['vitB9'] = self.get_float(data, 'vitB9')
        self.product.vitamins['vitB12'] = self.get_float(data, 'vitB12')

    def _build_microelements(self, data):  # витамины
        self.product.microelements['Ca'] = self.get_float(data, 'Ca')
        self.product.microelements['Fe'] = self.get_float(data, 'Fe')
        self.product.microelements['Mg'] = self.get_float(data, 'Mg')
        self.product.microelements['Phos'] = self.get_float(data, 'Phos')
        self.product.microelements['Kalis'] = self.get_float(data, 'Kalis')
        self.product.microelements['Na'] = self.get_float(data, 'Na')
        self.product.microelements['Zn'] = self.get_float(data, 'Zn')
        self.product.microelements['Cu'] = self.get_float(data, 'Cu')
        self.product.microelements['Mn'] = self.get_float(data, 'Mn')
        self.product.microelements['Se'] = self.get_float(data, 'Se')
        self.product.microelements['Fluor'] = self.get_float(data, 'Fluor')


class ProductUpdater(ProductBuilder):
    def __init__(self, product):
        super().__init__()
        self.product = product


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

    def get_update_values_str(self, obj):

        obj_dict = copy.deepcopy(obj.__dict__)
        name_value = ''
        for item in self.column_list[1:]:
            value = obj_dict.get(item,None)
            name_value = name_value + f', {item}={value}' if len(name_value) > 0 else f'{item}={value}'
        name_value = name_value.replace('None', 'NULL')
        item_id = int(obj_dict.get('product_id'))

        return name_value, item_id

    def update(self, obj):
        name_value, item_id = self.get_update_values_str(obj)

        statement = f"UPDATE {self.tablename} SET {name_value} WHERE id=?"

        self.cursor.execute(statement, (item_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

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

    def get_update_values_str(self, obj):
        name_value = ''
        obj_dict = copy.deepcopy(obj.__dict__)
        for item in self.column_list[1:]:
            value = obj_dict.get(item, None)
            name_value = name_value + f', {item}={value}' if len(name_value) > 0 else f'{item}={value}'
        name_value = name_value.replace('None', 'NULL')
        obj_id = obj_dict.get('id', None)
        return name_value, obj_id

    def update(self, obj):
        name_value, obj_id = self.get_update_values_str(obj)

        statement = f"UPDATE {self.tablename} SET {name_value} WHERE id=?"

        self.cursor.execute(statement, (obj_id,))
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


connection = sqlite3.connect('calc.sqlite3')


class ProductMapper(ItemMapper):

    def __init__(self, connection):

        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'product'
        self.column_list = list()
        self.column_list = self.get_column_list()
        super().__init__(connection, 'product')
        # print(self.column_list)

    def get_column_list(self):
        column_list = []
        for row in self.connection.execute(f"pragma table_info('product')").fetchall():
            column_list.append(row[1])
        return column_list

    def all(self):
        statement = f'SELECT * FROM {self.tablename} WHERE is_active = 1'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            # print(item)
            # id, category_id, name, is_active, kkal, water, proteins, fats, carbs = item

            product = Product()
            product.id = item[0]
            product.category = item[1]
            product.name = item[2]
            product.kkal = item[4]
            product.water = item[5]
            product.proteins = {}
            product.proteins['proteins'] = item[7]
            product.fats = {}
            product.fats['fats'] = item[26]
            product.carbs = {}
            product.carbs['carbs'] = item[63]
            result.append(product)
        # print(f'result = {result}')
        return result

    def filter(self, category=None):
        # print(f'filter. category = {category}')
        if category:
            statement = f'SELECT id, category_id, name, is_active, kkal, water, proteins, fats, carbs FROM {self.tablename} WHERE category_id = ? AND is_active = 1'
            self.cursor.execute(statement, (category,))
            result = []
            for item in self.cursor.fetchall():
                id, category_id, name, is_active, kkal, water, proteins, fats, carbs = item
                # print(item)
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
            return result
        else:
            return self.all()

    def get_cursor_tuple(self, obj):
        variables = obj.__dict__
        # print(variables)
        cursor_dict = {}
        cursor_list = []
        for item in self.column_list[1:]:
            if item in ['proteins', 'fats', 'carbs']:
                temp_dict = {}
                temp_dict = variables.get(item, None)
                cursor_dict.update(temp_dict)
            elif item == 'category_id':
                categ = variables.get('category', None)
                cursor_dict[item] = int(MapperRegistry.get_current_mapper('category').find_id_by_name(categ.name))
            elif item == 'is_active':
                cursor_dict[item] = 1
            else:
                if item not in cursor_dict:
                    cursor_dict[item] = variables.get(item, None)

        cursor_list = cursor_dict.values()
        cursor_tuple = tuple(cursor_list)
        return cursor_tuple

    def get_update_values_str(self, obj):
        product_dict = copy.deepcopy(obj.__dict__)
        pro_dict = {}
        for key, val in product_dict.items():
            if key in ['proteins', 'fats', 'carbs']:
                pro_dict.update(product_dict.get(key, None))

        product_dict.pop('proteins')
        product_dict.pop('fats')
        product_dict.pop('carbs')
        product_dict.update(pro_dict)
        name_value = ''
        for item in self.column_list[1:]:
            value = product_dict.get(item,None)
            if item == 'is_active':
                value = 1
            elif item == 'category_id':
                value = product_dict.get('category', None)
            elif item == 'name':
                value = product_dict.get('name', None)
                value = f"'{value}'"
            # print(f' {item}={value}')
            name_value = name_value + f', {item}={value}' if len(name_value) > 0 else f'{item}={value}'
        name_value = name_value.replace('None', 'NULL')
        item_id = int(product_dict.get('product_id'))

        return name_value, item_id

    def find_id_by_name(self, name):
        statement = f'SELECT id FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (name,))
        result = self.cursor.fetchone()
        # print(f'find_id_by_name.result = {result}')
        return result[0]

    def find_by_id(self, id):
        column_str = str(self.column_list)
        column_str = column_str.replace("'", "").replace('[', '').replace(']', '')

        statement = f'SELECT {column_str} FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()

        data = {}
        for i in range(len(self.column_list)):
            data[self.column_list[i]] = result[i]
        category = data['category_id']

        new_product = ProductBuilder()
        product_builder = DirectProductBuild()
        product_builder.constructor(new_product, data, category)

        if result:
            return new_product.product
        else:
            raise RecordNotFoundException(f'record with id={id} not found')


class UserMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'user'

    def is_admin(self, id):
        statement = f'SELECT isadmin FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        return True if result == 1 else False

    def check_password(self, login, pswd):
        # print(login)
        statement = f'SELECT password FROM {self.tablename} WHERE name=?'
        print(statement)
        self.cursor.execute(statement, (login,))
        result = self.cursor.fetchone()
        # print(result[0])
        # print(pswd)
        return True if result[0] == pswd else False


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'product': ProductMapper,
        'category': CategoryMapper,
        'user': UserMapper,
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
