import copy
from .users import Student
from .updater import Subject
from patterns.unit_of_work import DomainObject


# creating prototype for courses
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject, DomainObject):
    def __init__(self, name, category, location, start_date):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        self.location = location
        self.start_date = start_date
        super().__init__()

    def __repr__(self):
        return self.name

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()

    def update_location(self, location):
        self.location = location
        self.notify_location()

    def update_start_date(self, start_date):
        self.start_date = start_date
        self.notify_date()

    def get_location(self):
        return self.location

    def get_start_date(self):
        return self.start_date


# types of courses
class InteractiveCourse(Course):
    pass


class VideoCourse(Course):
    pass


# categories of courses
class CourseCategory(DomainObject):

    def __init__(self, name, category, category_id):
        self.category_id = category_id
        self.name = name
        self.category = category
        self.courses = []

    # count courses in a category
    def course_count(self) -> int:
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result

    def __repr__(self):
        return self.name


class CourseFactory:
    types = {
        'video': VideoCourse,
        'interactive': InteractiveCourse,
    }

    @classmethod
    def create(cls, type_, name, category, location, start_date):
        return cls.types[type_](name, category, location, start_date)

