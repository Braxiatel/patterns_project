from service import add_closing_slash
from .requests_handler import GetRequests, PostRequests
import quopri
from patterns.logger import Logger

logger = Logger('main')


class PageNotFound404:
    def __call__(self, request):
        return '404 NOT', '404 PAGE NOT FOUND'


class Framework:
    """Framework class"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):

        # finding a path that was requested
        path = add_closing_slash(environ['PATH_INFO'])

        request = {}
        method, request['method'] = environ['REQUEST_METHOD'], environ['REQUEST_METHOD']

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = Framework.decode_value(data)
            logger.log(f'Got POST request: {Framework.decode_value(data)}')
        elif method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            logger.log(f'Got GET request: {request_params}')

        # checking how to serve this path
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # checking front controller
        for front in self.fronts_lst:
            front(request)

        # generating response
        status, body = view(request)
        response_headers = [
            ('Content-Type', 'text/html')
        ]

        start_response(status, response_headers)
        return [body.encode('utf-8')]

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data

