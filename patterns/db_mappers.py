from random import randint
from patterns.logger import Logger
from patterns.users import Student
from patterns.courses import CourseCategory


logger = Logger('db_mappers')


class StudentMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            student_id, name, email = item
            student = Student(name=name, email=email)
            student.id = student_id
            result.append(student)
        return result

    def get_student_by_id(self, student_id):
        statement = f'SELECT id, name, email FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (student_id, ))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'Record with {student_id} is not found')

    def get_student_by_name(self, student_name):
        statement = f'SELECT name, email FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (student_name, ))
        result = self.cursor.fetchone()
        logger.log(f"Got result of execution {result}")
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'Record with {student_name} is not found')

    def get_id_by_name(self, student_name):
        statement = f'SELECT id FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (student_name,))
        return self.cursor.fetchone()

    def insert(self, obj):
        user_id = randint(1000, 5000)
        statement = f'INSERT INTO {self.tablename} (id, name, email) VALUES (?, ?, ?)'
        self.cursor.execute(statement, (user_id, obj.name, obj.email))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBCommitException(e.args)

    def update(self, obj):
        # id is not present in Student class, so take it from db
        student_id = self.get_id_by_name(obj.name)[0]
        statement = f'UPDATE {self.tablename} SET email=? WHERE id=?'
        self.cursor.execute(statement, (obj.email, student_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBDeleteException(e.args)


class CategoryMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'category'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            category_id, category, name = item
            category = CourseCategory(name=name, category=category, category_id=category_id)
            result.append(category)
        return result

    def insert(self, obj):
        statement = f'INSERT INTO {self.tablename} (name, category, category_id ) VALUES (?, ?, ?)'
        self.cursor.execute(statement, (obj.name, obj.category, obj.category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBCommitException(e.args)

    def update(self, obj):
        statement = f'UPDATE {self.tablename} SET name=? WHERE category_id=?'
        self.cursor.execute(statement, (obj.name, obj.category_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE category_id=?'
        self.cursor.execute(statement, (obj.category_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBDeleteException(e.args)


class DBCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'DB commit error {message}')


class DBUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'DB update error {message}')


class DBDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'DB delete error {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
