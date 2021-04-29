from service import add_closing_slash


class PageNotFound404:
    def __call__(self, request):
        return '404 NOT', '404 PAGE NOT FOUND'


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):

        # finding a path that was requested
        path = environ['PATH_INFO']
        path = add_closing_slash(path)

        # checking how to serve this path
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        request = {}
        for front in self.fronts_lst:
            front(request)

        # generating response
        status, body = view(request)
        response_headers = [
            ('Content-Type', 'text/html')
        ]

        start_response(status, response_headers)
        return [body.encode('utf-8')]

