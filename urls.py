from datetime import date
from views import Index, About, Register
from uuid import uuid4


# front controller
def get_date(request):
    request['date'] = date.today()


def get_key(request):
    request['random_string'] = uuid4()


fronts = [get_date, get_key]

routes = {
    '/': Index(),
    '/about/': About(),
    '/register/': Register(),
}
