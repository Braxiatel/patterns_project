from datetime import date
from uuid import uuid4
from patterns.logger import FileLogger

file_logger = FileLogger('urls', 'test.log')


# front controller
def get_date(request):
    request['date'] = date.today()


def get_key(request):
    request['random_string'] = uuid4()


def get_name(request):
    file_logger.log('Getting name for a user')
    try:
        request['name'] = request['data']['feedback_name']
    except KeyError:
        request['name'] = 'Anonymous'


fronts = [get_date, get_key, get_name]
