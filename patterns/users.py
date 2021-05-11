class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        print(f"This is a User {self.name}")


class Teacher(User):
    pass


class Student(User):
    pass


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
