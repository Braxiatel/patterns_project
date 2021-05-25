from random import randint
import json
from patterns.logger import Logger
from patterns.users import Student
from patterns.courses import CourseCategory, Course


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
            category_id, category, name, courses = item
            courses = json.loads(courses)
            category = CourseCategory(name=name, category=category, category_id=category_id)
            category.courses.extend(courses)
            result.append(category)
        return result

    def get_category_by_name(self, category_name):
        statement = f'SELECT name, category, category_id FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (category_name, ))
        result = self.cursor.fetchone()
        logger.log(f"Got result of execution {result}")
        if result:
            return CourseCategory(*result)
        else:
            raise RecordNotFoundException(f'Record with {category_name} is not found')

    def get_category_by_id(self, category_id):
        statement = f'SELECT name, category, category_id FROM {self.tablename} WHERE category_id=?'
        self.cursor.execute(statement, (category_id, ))
        result = self.cursor.fetchone()
        logger.log(f"Got result of execution {result}")
        if result:
            return CourseCategory(*result)
        else:
            raise RecordNotFoundException(f'Record with {category_id} is not found')

    def get_courses_from_category(self, category_id):
        statement = f'SELECT courses FROM {self.tablename} WHERE category_id=?'
        self.cursor.execute(statement, (category_id,))
        try:
            result = self.cursor.fetchone()[0]
            return result if result else '[]'
        except TypeError:
            return '[]'

    def insert(self, obj):
        courses = '[]'
        statement = f'INSERT INTO {self.tablename} (name, category, category_id, courses ) VALUES (?, ?, ?, ?)'
        self.cursor.execute(statement, (obj.name, obj.category, obj.category_id, courses))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBCommitException(e.args)

    def update(self, obj):
        db_courses = self.get_courses_from_category(obj.category_id)
        db_courses = json.loads(db_courses)

        # appending new course to the existing list of courses
        db_courses.append(obj.courses[-1].name)

        # dumping it to store in appropriate format
        dumped_courses = json.dumps(db_courses)
        logger.log(f'Appending new courses {dumped_courses} to category')
        statement = f'UPDATE {self.tablename} SET courses=? WHERE name=?'
        self.cursor.execute(statement, (dumped_courses, obj.name))
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


class CourseMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'course'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []

        for item in self.cursor.fetchall():
            course_id, name, category, location, start_date = item
            category = CategoryMapper(self.connection).get_category_by_id(category)
            course = Course(name=name, category=category,
                            location=location, start_date=start_date)
            course.course_id = course_id
            logger.log(f'Got course {course}')
            result.append(course)
        return result

    def insert(self, obj):
        course_id = randint(1000, 5000)
        statement = f'INSERT INTO {self.tablename} (course_id, name, category, location, start_date) VALUES (?, ?, ?, ?, ?)'
        self.cursor.execute(statement, (course_id, obj.name, obj.category.category_id,
                                        obj.location, obj.start_date))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBCommitException(e.args)

    def get_id_by_name(self, course_name):
        statement = f'SELECT course_id FROM {self.tablename} WHERE name=?'
        self.cursor.execute(statement, (course_name,))
        return self.cursor.fetchone()

    def update(self, obj):
        # id is not present in Student class, so take it from db
        course_id = self.get_id_by_name(obj.name)[0]
        statement = f'UPDATE {self.tablename} SET name=?, location=?, start_date=? WHERE course_id=?'
        self.cursor.execute(statement, (obj.name, obj.location, obj.start_date, course_id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBUpdateException(e.args)

    def delete(self, obj):
        statement = f'DELETE FROM {self.tablename} WHERE course_id=?'
        self.cursor.execute(statement, (obj.course_id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DBDeleteException(e.args)

    def get_course_by_name(self, course_name):
        statement = f'SELECT name, category, location, start_date FROM {self.tablename} WHERE name=?'
        try:
            self.cursor.execute(statement, (course_name, ))
            result = self.cursor.fetchone()

            logger.log(f"Got result of execution {result} and type {type(result)}")
            if result:
                # rebuilding 'result', because category is stored in db as id (int),
                # but Course class requires Category (user class) as input
                category = CategoryMapper(self.connection).get_category_by_id(result[1])
                new_result = [result[0], category, result[2], result[3]]
                return Course(*new_result)
            else:
                raise RecordNotFoundException(f'Record with name {course_name} not found')
        except Exception as e:
            raise RecordNotFoundException(f'Record not found: {e}')


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
