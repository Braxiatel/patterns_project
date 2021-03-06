from patterns.unit_of_work import DomainObject


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return self.name


class Teacher(User):
    pass


class Student(User, DomainObject):

    def __init__(self, name, email):
        self.courses = []
        super().__init__(name, email)

    def update_email(self, email):
        self.email = email


class Admin(User):
    pass


# abstract factory to create new users
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
        'admin': Admin,
    }

    @classmethod
    def create(cls, type_, name, email):
        return cls.types[type_](name, email)
