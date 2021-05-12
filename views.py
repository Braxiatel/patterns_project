from datetime import date
from random import randint
from zorro_framework.template_reader import render
from patterns.engine import Engine
from patterns.logger import Logger, FileLogger
from patterns.decorators import timer, app_route

website_engine = Engine()
logger = Logger('views')
file_logger = FileLogger('views', 'test.log')
routes = {}


@app_route(routes=routes, url='/')
class Index:
    @timer(name="Index")
    def __call__(self, request):
        file_logger.log('Index page with schedules')
        return '200 OK', render('index.html', date=date.today())


@app_route(routes=routes, url='/categories/')
class Categories:
    @timer(name="Categories")
    def __call__(self, request):
        logger.log(f'Got list of categories: {website_engine.categories}')
        return '200 OK', render('categories.html', objects_list=website_engine.categories)


@app_route(routes=routes, url='/register/')
class Register:
    @timer(name="Register")
    def __call__(self, request):
        return '200 OK', render('register.html', random_string=request.get('random_string', None))


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
class CoursesList:
    @timer(name="CourseList")
    def __call__(self, request):
        try:
            logger.log(f'Got list of courses: {website_engine.courses}')
            return '200 OK', render('courses.html',
                                    number_of_categories=len(website_engine.categories),
                                    object_list=website_engine.courses)
        except IndexError:
            return '200 OK', render('empty_base.html', name='courses')


@app_route(routes=routes, url='/new_course/')
class NewCourse:
    @timer(name="NewCourse")
    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']
            logger.log(f'POST request for new course contains data: {data}')

            name = data['name']
            name = website_engine.decode_value(name)
            category_name = data['category']
            category = website_engine.get_category_by_name(category_name)

            course = website_engine.create_course(type_='video', name=name, category=category)
            website_engine.courses.append(course)

            logger.log(f'Course {course} has been successfully created')
            logger.log(f'Course is written into {course.category.category_id}')
            return '200 OK', render('courses.html',
                                    object_list=website_engine.courses,
                                    number_of_categories=len(website_engine.categories))
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

            return '200 OK', render('categories.html', objects_list=website_engine.categories)
        else:
            categories = website_engine.categories
            return '200 OK', render('new_category.html', categories=categories)


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
            return '200 OK', render('courses.html', object_list=website_engine.courses)
        except KeyError:
            return '200 OK', render('empty_base.html', name='courses')


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
            logger.log(f'POST request for new course contains data: {data}')

            name = data['name']
            name = website_engine.decode_value(name)
            email = data['email']
            role = data['role']

            if role == 'student':
                user = website_engine.create_user(type_=role, name=name, email=email)
                website_engine.students.append(user)
                logger.log(website_engine.students)
            elif role == 'teacher':
                user = website_engine.create_user(type_=role, name=name, email=email)
                website_engine.teachers.append(user)
                logger.log(website_engine.teachers)
            return '200 OK', render('index.html', date=date.today())
        # if method is GET
        else:
            return '200 OK', render('signup.html', categories_list=website_engine.categories)

