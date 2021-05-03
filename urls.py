from datetime import date
from views import Index, About, Register
from uuid import uuid4


# front controller
def get_date(request):
    request['date'] = date.today()


def get_key(request):
    request['random_string'] = uuid4()


def get_available_routes(request):
    available_routes = ", ".join([d for d in routes.keys()])
    request['available_routes'] = available_routes


fronts = [get_date, get_key, get_available_routes]

routes = {
    '/': Index(),
    '/about/': About(),
    '/register/': Register(),
}
