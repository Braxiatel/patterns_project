from patterns.db_mappers import StudentMapper, CategoryMapper, CourseMapper
from patterns.users import Student
from patterns.courses import CourseCategory, Course
from patterns.logger import Logger
import sqlite3

logger = Logger('mapper_registry')
connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    mappers = {
        'student': StudentMapper,
        'category': CategoryMapper,
        'course': CourseMapper,
    }

    @staticmethod
    def get_mapper(obj):
        logger.log(f"Got class for mapping {obj.__class__}")
        if isinstance(obj, Student):
            return StudentMapper(connection)
        elif isinstance(obj, CourseCategory):
            return CategoryMapper(connection)
        elif isinstance(obj, Course):
            return CourseMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
