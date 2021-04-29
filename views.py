from zorro_framework.template_reader import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'


class Register:
    def __call__(self, request):
        return '200 OK', render('register.html', random_string=request.get('random_string', None))


class NotFound404:
    def __call__(self, request):
        return '404 NOK', '404 PAGE NOT FOUND'
