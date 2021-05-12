class FakeApplication:
    def __call__(self, environ, start_response):
        status, body = "200 OK", "Hello from Fake"
        response_headers = [
            ('Content-Type', 'text/html')
        ]

        start_response(status, response_headers)
        return [body.encode('utf-8')]
