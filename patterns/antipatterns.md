Antipatterns
============

## Антипаттерны в коде

### Magic Number

Не найдено

### Spaghetti code

```
class NewCourse:
    @timer(name="NewCourse")
    def __call__(self, request):
        mapper = MapperRegistry.get_current_mapper('category')
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
            category = mapper.get_category_by_name(category_name=category_name)

            course = website_engine.create_course(type_='video', name=name, category=category,
                                                  location=location, start_date=start_date)

            category.courses.append(course)
            category.mark_dirty()
            course.mark_new()
            UnitOfWork.get_thread().commit()
            logger.log(f'Successfully added new category {course}')

            course.observers.append(email_notifier)
            course.observers.append(sms_notifier)

            mapper = MapperRegistry.get_current_mapper('course')
            courses = mapper.all()
            logger.log(f'Course {course} has been successfully created')
            logger.log(f'Course is written into {course.category.category_id}')
            return '200 OK', render('courses.html',
                                    objects_list=courses,
                                    courses_count=len(courses))
        # if method is GET
        else:
            categories = mapper.all()
            if categories:
                return '200 OK', render('new_course.html', categories_list=categories)
            else:
                return '200 OK', render('empty_base.html', name='categories')

```

class `NewCourse` был похож на спагетти, возможно из-за того, что на странице требовалось большое количество разных данных и с добавлением БД стало сложно понимать как происходит обработка страницы `NewCourse`. После того как эта страница была переписана под стиль ClassView, структура стала более понятной. 

```

class NewCourse(CreateView):
    template_name = 'new_course.html'

    def create_object(self, data: dict):
        name = data['name']
        name = website_engine.decode_value(name)
        location = data['location']
        location = website_engine.decode_value(location)
        start_date = data['start_date']
        start_date = website_engine.decode_value(start_date)
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

        course.observers.append(email_notifier)
        course.observers.append(sms_notifier)

    def get_context_data(self):
        mapper = MapperRegistry.get_current_mapper('course')
        courses = mapper.all()
        context_data = super().get_context_data()
        context_data['objects_list'] = courses
        context_data['courses_count'] = [len(courses)]
        categories = MapperRegistry.get_current_mapper('category')
        categories_list = categories.all()
        context_data['categories_list'] = categories_list
        context_data['categories_count'] = [len(categories_list)]
        return context_data

    def template_for_post_request(self):
        self.set_template_name('courses.html')

    def template_for_get_request(self):
        self.set_template_name('new_course.html')
```

### Lasagna Code

Не найдено

### Blind faith

Почти полностью отсутствует проверка корректности входных данных. Необходимо написать множество функций, которые бы обрабатывали входные данные. 
Например, можно создать функцию `check_length`, которая бы проверяла длину вводимых данных. Функция бы вызывалась в `views` для полей, где необходима эта проверка. Это будет выглядеть приблизительно так:

```
name = data['name']
try:
    website_engine.check_length(name, max_length=15)
except ValidationError:
    error_text = 'Name exceeds 15 symbols. Please provide shorter name.' 

```

### Cryptic Code

Не найдено

### Hard Code

В функции `get_course_by_name` в модуле `db_mappers` есть строчка, где захардкожены результаты запроса. То есть, если порядок в изначальном запросе поменяется, то и последующая функция сломается.

`new_result = [result[0], category, result[2], result[3]]`

Возможно здесь лучше использовать **namedTuple**.

### Soft Code

Не найдено

### Lava Flow

Не найдено

## Специфические для Python антипаттерны в коде

### Asking for permission instead of forgiveness
```
def get_course_by_name(self, course_name):
    statement = f'SELECT name, category, location, start_date FROM {self.tablename} WHERE name=?'
    self.cursor.execute(statement, (course_name, ))
    result = self.cursor.fetchone()

    if result:
        [...]
        return Course(*new_result)
    else:
        raise RecordNotFoundException(f'Record with {course_name} is not found')
```
Пример, когда необходимо использовать `try ... except` но был использован `if ... else` и отсутствовала обработка ошибок от запроса.

## Антипаттерны ООП
### Anemic Domain Model

Не найдено

### God object (The Blob)

Не найдено

### Poltergeist

Не найдено

### Singletonitis

Не найдено

### Privatization 

Не найдено

## Методологические антипаттерны

### Copy — Paste

Большое количество повторяющихся вещей было замечено в модуле `views`. Это связано с тем, что не все страницы были переписаны под ClassView.
Теперь эта ситуация исправлена и большая часть страниц обрабатывается с помощью классов. По-прежнему осталась только страница `CourseCopy`, поскольку она работает иначе, чем остальные и нет смысле писать под неё специальный classView. 


### Dead Code

* Переменная, параметр, поле, метод или класс больше не используются (чаще всего потому, что устарели).

Переменная `init_id` в классе `CourseCategory`. Оказалось что нигде не используется. Создание id категории было перенесено на другой слой, однако здесь осталось неудалённым.


### Golden hammer

Не найдено 


### Improbability factor

Поскольку у меня стоит Unique Constraint на поле название курса, есть большая вероятность, что при создании нового курса сработает эта ошибка, однако она никаким образом не обрабатывалась.
Теперь это поправлено:

```

    try:
        name = request_params['name']
        [...]
    except IntegrityError:
        return '400 NOK', render('error_page.html',
                                  error_text=f'Unable to copy course: course with this name already exists')    
```

### Premature optimization

Не найдено

### Reinventing the square wheel

Функция `get_course_by_name` оказалась квадратным колесом так как есть лучшее решение этой задачи с помощью правильного запроса в БД.
