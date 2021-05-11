import quopri
from .users import UserFactory
from .courses import CourseFactory, CourseCategory


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name, email):
        return UserFactory.create(type_, name, email)

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    @staticmethod
    def create_category(name, category_id, category=None):
        return CourseCategory(name, category, category_id)

    def get_category_by_id(self, category_id):
        for category in self.categories:
            if category.category_id == category_id:
                return category
        raise Exception(f"Category with id {category_id} is not found")

    def get_category_by_name(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return category
        raise Exception(f"Category with name {category_name} is not found")

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

