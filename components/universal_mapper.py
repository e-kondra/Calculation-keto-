import abc
import copy


class ItemMapper(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def tablename(self):
        pass

    @property
    @abc.abstractmethod
    def model(self):
        pass

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.column_list = list()
        self.column_list = self.get_column_list()

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        column_names = [description_info[0] for description_info in self.cursor.description]
        result = []

        for values in self.cursor.fetchall():
            object = self.model(**{column_names[i]: values[i] for i,_ in enumerate(values)})
            result.append(object)
        return result

    def insert(self, **schema):
        statement = f"INSERT INTO {self.tablename} ({','.join(schema.keys())}) VALUES (?)"
        self.cursor.execute(statement, (','.join(schema.values()),))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


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

    def find_by_id(self, id):
        statement = f'SELECT id, name FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return self.model(result[1])
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def find_id_by_name(self, name):
        statement = f'SELECT id FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (name,))
        return self.cursor.fetchone()[0]


    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


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