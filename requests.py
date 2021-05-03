import cgi


class GetRequests:

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params


class PostRequests:

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = parse_input_data(data_str)
        return result

    def get_request_params(self, environ) -> dict:
        data = self.get_wsgi_input_data(environ)
        dict_data = self.parse_wsgi_input_data(data)
        return dict_data


def parse_input_data(data: str) -> dict:
    result = {}
    print(f'Got data in Request: {data}')
    if data:
        params = data.split('&')
        for item in params:
            k, v = item.split('=')
            result[k] = v
    return result
