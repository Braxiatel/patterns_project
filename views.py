from datetime import date
from random import randint
from sqlite3 import IntegrityError
from zorro_framework.template_reader import render
from patterns.engine import Engine
from patterns.validators import Validator, ValidationException
from patterns.logger import Logger
from patterns.mapper_registry import MapperRegistry
from patterns.decorators import timer, app_route
from patterns.views_templates import ListView, CreateView, UpdateView
from patterns.api_module import BaseSerializer
from patterns.updater import EmailNotify, SMSNotify
from patterns.unit_of_work import UnitOfWork
from patterns.db_mappers import RecordNotFoundException

website_engine = Engine()
logger = Logger('views')
email_notifier = EmailNotify()
sms_notifier = SMSNotify()
validator = Validator()
UnitOfWork.new_thread()
UnitOfWork.get_thread().set_mapper_registry(MapperRegistry)
routes = {}


@app_route(routes=routes, url='/')
class Index:
    @timer(name="Index")
    def __call__(self, request):
        return '200 OK', render('index.html', date=date.today())


@app_route(routes=routes, url='/categories/')
class Categories(ListView):
    template_name = 'categories.html'

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('category')
        categories = mapper.all()
        logger.log(f'Got result from db {categories}')

        context = super().get_context_data()
        context['categories_count'] = [len(categories)]
        if categories:
            context['objects_list'] = categories
        return context


@app_route(routes=routes, url='/register/')
class StudentCourseRegister(CreateView):
    template_name = 'register.html'

    def get_context_data(self):
        context = super().get_context_data()
        student_mapper = MapperRegistry.get_current_mapper('student')
        students = student_mapper.all()
        student_mapper = MapperRegistry.get_current_mapper('course')
        courses = student_mapper.all()
        context['courses'], context['students'] = courses, students
        context['courses_count'] = [len(courses)]
        context['students_count'] = [len(students)]
        return context

    def create_object(self, data: dict):
        student_mapper = MapperRegistry.get_current_mapper('student')
        course_mapper = MapperRegistry.get_current_mapper('course')
        course_name = data['course_name']
        course_name = website_engine.decode_value(course_name)
        course = course_mapper.get_course_by_name(course_name)
        student_name = data['student_name']
        student_name = website_engine.decode_value(student_name)
        student = student_mapper.get_student_by_name(student_name)
        course.add_student(student)
        logger.log(f'Students on course: {course.students}')


@app_route(routes=routes, url='/feedback/')
class Feedback:
    @timer(name="Feedback")
    def __call__(self, request):
        return '200 OK', render('feedback.html', name=request.get('name', None))


class NotFound404:
    @timer(name="NotFound")
    def __call__(self, request):
        return render('error_page.html', error_text='404 PAGE NOT FOUND')


@app_route(routes=routes, url='/courses/')
class CoursesList(ListView):
    template_name = 'courses.html'

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('course')
        courses = mapper.all()
        logger.log(f'got courses: {courses}')

        context_data = super().get_context_data()
        context_data['courses_count'] = [len(courses)]
        if courses:
            context_data['objects_list'] = courses
        return context_data


@app_route(routes=routes, url='/new_course/')
class NewCourse(CreateView):
    template_name = 'new_course.html'
    validation_error = ''
    success_text = ''

    def create_object(self, data: dict):
        course_mapper = MapperRegistry.get_current_mapper('course')
        try:
            name = data['name']
            name = website_engine.decode_value(name)
            validator.word_validation(name)
            try:
                if course_mapper.get_course_by_name(name):
                    self.validation_error = f'Course with this name: {name} already exists'
                    raise ValidationException(f'Course with this name: {name} already exists')
            except RecordNotFoundException:
                pass
            location = data['location']
            location = website_engine.decode_value(location)
            validator.word_validation(location)
            start_date = data['start_date']
            start_date = website_engine.decode_value(start_date)
            validator.date_validation(start_date)

            category_name = data['category']
            mapper = MapperRegistry.get_current_mapper('category')
            category = mapper.get_category_by_name(category_name=category_name)

            course = website_engine.create_course(type_='video', name=name, category=category,
                                                  location=location, start_date=start_date)

            category.courses.append(course)
            category.mark_dirty()
            course.mark_new()
            UnitOfWork.get_thread().commit()
            logger.log(f'Course {course} has been successfully created')
            self.success_text = f'Successfully added course {course}!'

            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)
        except ValidationException as e:
            logger.log(f'Validation failed: {e}')
            self.validation_error = e

    def get_context_data(self):
        course_mapper = MapperRegistry.get_current_mapper('course')
        courses = course_mapper.all()
        context_data = super().get_context_data()
        context_data['objects_list'] = courses
        context_data['courses_count'] = [len(courses)]
        categories = MapperRegistry.get_current_mapper('category')
        categories_list = categories.all()
        context_data['categories_list'] = categories_list
        context_data['categories_count'] = [len(categories_list)]
        context_data['validation_error'] = [self.validation_error]
        context_data['success_text'] = [self.success_text]
        self.validation_error = ''
        self.success_text = ''
        return context_data

    def template_for_post_request(self):
        if self.success_text != '':
            self.set_template_name('courses.html')

    def template_for_get_request(self):
        self.set_template_name('new_course.html')


@app_route(routes=routes, url='/new_category/')
class NewCategory(CreateView):
    template_name = 'new_category.html'

    def create_object(self, data: dict):
        category_name = data['name']
        category_name = website_engine.decode_value(category_name)
        category_id = randint(1000, 5000)
        category = None

        new_category = website_engine.create_category(name=category_name, category=category, category_id=category_id)
        new_category.mark_new()
        UnitOfWork.get_thread().commit()
        logger.log(f'Successfully added new category {new_category}')

    def template_for_post_request(self):
        self.set_template_name('categories.html')

    def template_for_get_request(self):
        self.set_template_name('new_category.html')

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('category')
        categories = mapper.all()
        context = super().get_context_data()
        context['objects_list'] = categories
        context['categories_count'] = [len(categories)]
        return context


@app_route(routes=routes, url='/copy-course/')
class CourseCopy:
    @timer(name="CourseCopy")
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            logger.log(f'copying the course {name}')
            mapper = MapperRegistry.get_current_mapper('course')
            existing_course = mapper.get_course_by_name(name)
            if existing_course:
                new_name = f'{name}_copy'
                new_course = existing_course.clone()
                new_course.name = new_name
                new_course.mark_new()
                UnitOfWork.get_thread().commit()
            courses = mapper.all()
            logger.log(f"new list of courses is {courses}")
            courses_count = [len(courses)]
            return '200 OK', render('courses.html', objects_list=courses,
                                    courses_count=courses_count)
        except IntegrityError:
            return '400 NOK', render('error_page.html',
                                     error_text=f'Unable to copy course: course with this name already exists')
        except Exception as e:
            return '400 NOK', render('error_page.html', error_text=f'Unable to copy course: {e}')


@app_route(routes=routes, url='/course_update/')
class CourseUpdate(UpdateView):
    template_name = 'course_update.html'

    def get_context_data(self):
        context = super().get_context_data()
        course_mapper = MapperRegistry.get_current_mapper('course')
        courses = course_mapper.all()
        context['courses'] = courses
        context['courses_count'] = [len(courses)]
        return context

    def update_object(self, data: dict):
        course_name = data['course_name']
        course_mapper = MapperRegistry.get_current_mapper('course')
        course = course_mapper.get_course_by_name(course_name)
        location = data['location']
        start_date = data['start_date']
        course.update_location(location)
        course.update_start_date(start_date)
        course.mark_dirty()
        UnitOfWork.get_thread().commit()


@app_route(routes=routes, url='/signup/')
class Signup(CreateView):
    template_name = 'signup.html'

    def create_object(self, data: dict):
        name = data['name']
        name = website_engine.decode_value(name)
        email, role = data['email'], data['role']

        if role == 'student':
            user = website_engine.create_user(type_=role, name=name, email=email)
            user.mark_new()
            UnitOfWork.get_thread().commit()
        elif role == 'teacher':
            user = website_engine.create_user(type_=role, name=name, email=email)
            website_engine.teachers.append(user)
            logger.log(website_engine.teachers)

    def template_for_post_request(self):
        self.set_template_name('student_list.html')

    def template_for_get_request(self):
        self.set_template_name('signup.html')

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('student')
        user_students = mapper.all()
        context = super().get_context_data()
        context['students'] = user_students
        context['students_count'] = [len(user_students)]
        return context


@app_route(routes=routes, url='/student_list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('student')
        user_students = mapper.all()
        logger.log(f'Got result from db {user_students}')
        context_data = super().get_context_data()
        context_data['students'] = user_students
        context_data['students_count'] = [len(user_students)]
        return context_data


@app_route(routes=routes, url='/student_update/')
class StudentUpdateView(UpdateView):
    template_name = 'student_update.html'

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('student')
        user_students = mapper.all()
        logger.log(f'Got result from db {user_students}')
        context = super().get_context_data()
        context['students'] = user_students
        context['students_count'] = [len(user_students)]
        return context

    def update_object(self, data: dict):
        email = data['email']
        student_name = data['student_name']
        student_name = website_engine.decode_value(student_name)

        mapper = MapperRegistry.get_current_mapper('student')
        student = mapper.get_student_by_name(student_name)

        student.update_email(email)
        student.mark_dirty()
        UnitOfWork.get_thread().commit()
        logger.log(f'Now the student is: {student}')

    def template_for_post_request(self):
        self.set_template_name('student_list.html')

    def template_for_get_request(self):
        self.set_template_name('student_update.html')


@app_route(routes=routes, url='/api/')
class CourseApi:
    @timer(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(website_engine.courses).save()
