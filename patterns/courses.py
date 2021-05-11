import copy


# creating prototype for courses
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def __repr__(self):
        return self.name


# types of courses
class InteractiveCourse(Course):
    pass


class VideoCourse(Course):
    pass


# categories of courses
class CourseCategory:
    # id is needed for lookup
    init_id = 0

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
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)

