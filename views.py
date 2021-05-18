from datetime import date
from random import randint
from zorro_framework.template_reader import render
from patterns.engine import Engine
from patterns.logger import Logger, FileLogger
from patterns.decorators import timer, app_route
from patterns.views_templates import ListView, CreateView
from patterns.api_module import BaseSerializer
from patterns.updater import EmailNotify, SMSNotify

website_engine = Engine()
logger = Logger('views')
file_logger = FileLogger('views', 'test.log')
email_notifier = EmailNotify()
sms_notifier = SMSNotify()
routes = {}


@app_route(routes=routes, url='/')
class Index:
    @timer(name="Index")
    def __call__(self, request):
        file_logger.log('Index page with schedules')
        return '200 OK', render('index.html', date=date.today())


@app_route(routes=routes, url='/categories/')
class Categories(ListView):
    template_name = 'categories.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories_count'] = [len(website_engine.categories)]
        if website_engine.categories:
            context['objects_list'] = website_engine.categories
        return context


@app_route(routes=routes, url='/register/')
class StudentCourseRegister(CreateView):
    template_name = 'register.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = website_engine.courses
        context['students'] = website_engine.students
        context['courses_count'] = [len(website_engine.courses)]
        context['students_count'] = [len(website_engine.students)]
        return context

    def create_object(self, data: dict):
        course_name = data['course_name']
        course_name = website_engine.decode_value(course_name)
        course = website_engine.get_course(course_name)
        student_name = data['student_name']
        student_name = website_engine.decode_value(student_name)
        student = website_engine.get_student(student_name)
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
        context_data = super().get_context_data()
        context_data['courses_count'] = [len(website_engine.categories)]
        if website_engine.courses:
            context_data['objects_list'] = website_engine.courses
        return context_data


@app_route(routes=routes, url='/new_course/')
class NewCourse:
    @timer(name="NewCourse")
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']
            logger.log(f'POST request for new course contains data: {data}')

            name = data['name']
            name = website_engine.decode_value(name)
            location = data['location']
            location = website_engine.decode_value(location)
            start_date = data['start_date']
            start_date = website_engine.decode_value(start_date)
            category_name = data['category']
            category = website_engine.get_category_by_name(category_name)

            course = website_engine.create_course(type_='video', name=name, category=category,
                                                  location=location, start_date=start_date)
            website_engine.courses.append(course)

            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)

            logger.log(f'Course {course} has been successfully created')
            logger.log(f'Course is written into {course.category.category_id}')
            return '200 OK', render('courses.html',
                                    objects_list=website_engine.courses,
                                    courses_count=len(website_engine.courses))
        # if method is GET
        else:
            if website_engine.categories:
                return '200 OK', render('new_course.html', categories_list=website_engine.categories)
            else:
                return '200 OK', render('empty_base.html', name='categories')


@app_route(routes=routes, url='/new_category/')
class NewCategory:
    @timer(name="NewCategory")
    def __call__(self, request):
        if request['method'] == 'POST':
            # get name from request, create category_id
            data = request['data']
            logger.log(f'Getting {data} data from NewCategory view method')
            name = data['name']
            name = website_engine.decode_value(name)
            category_id = randint(1000, 5000)
            category = None

            new_category = website_engine.create_category(name=name, category=category, category_id=category_id)
            website_engine.categories.append(new_category)
            logger.log(f'Successfully added new category {new_category}')
            categories_count = [len(website_engine.categories)]

            return '200 OK', render('categories.html', objects_list=website_engine.categories,
                                    categories_count=categories_count)
        else:
            return '200 OK', render('new_category.html', categories=website_engine.categories)


@app_route(routes=routes, url='/copy-course/')
class CourseCopy:
    @timer(name="CourseCopy")
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            logger.log(f'copying the course {name}')
            existing_course = website_engine.get_course(name)
            if existing_course:
                new_name = f'{name}_copy'
                new_course = existing_course.clone()
                new_course.name = new_name
                website_engine.courses.append(new_course)
            logger.log(f"new list of courses is {website_engine.courses}")
            courses_count = [len(website_engine.courses)]
            return '200 OK', render('courses.html', object_list=website_engine.courses,
                                    courses_count=courses_count)
        except KeyError:
            return '200 OK', render('empty_base.html', name='courses')


@app_route(routes=routes, url='/course_update/')
class CourseUpdate(CreateView):
    template_name = 'course_update.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = website_engine.courses
        context['courses_count'] = [len(website_engine.courses)]
        return context

    def create_object(self, data: dict):
        course_name = data['course_name']
        course = website_engine.get_course(course_name)
        location = data['location']
        start_date = data['start_date']
        course.update_location(location)
        course.update_start_date(start_date)
        logger.log(f'Now the course is: {course}')


@app_route(routes=routes, url='/empty_page/')
class EmptyPage:
    def __call__(self, request):
        return '200 OK', 'Just an empty page.'


@app_route(routes=routes, url='/signup/')
class Signup:
    @timer(name="SignUp")
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = website_engine.decode_value(name)
            email = data['email']
            role = data['role']

            if role == 'student':
                user = website_engine.create_user(type_=role, name=name, email=email)
                website_engine.students.append(user)
            elif role == 'teacher':
                user = website_engine.create_user(type_=role, name=name, email=email)
                website_engine.teachers.append(user)
                logger.log(website_engine.teachers)

            return '200 OK', render('student_list.html', objects_list=website_engine.students,
                                    students_count=[len(website_engine.students)])
        # if method is GET
        else:
            return '200 OK', render('signup.html', categories_list=website_engine.categories)


@app_route(routes=routes, url='/student_list/')
class StudentListView(ListView):
    template_name = 'student_list.html'

    def get_context_data(self):
        if website_engine.students:
            context_data = super().get_context_data()
            context_data['objects_list'] = website_engine.students
            context_data['students_count'] = [len(website_engine.students)]
            return context_data
        else:
            context_data = super().get_context_data()
            context_data['students_count'] = [len(website_engine.students)]
            return context_data


@app_route(routes=routes, url='/api/')
class CourseApi:
    @timer(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(website_engine.courses).save()
