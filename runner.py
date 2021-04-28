from zorro_framework.main import Framework
from urls import routes, fronts
import argparse
from wsgiref.simple_server import make_server

parser = argparse.ArgumentParser(description='Simple implementation of web server.')
parser.add_argument("-p", "--port", help="Choose a port.", default=8000, type=int)
args = parser.parse_args()

application = Framework(routes, fronts)

try:
    with make_server('', args.port, application) as httpd:
        print(f"Running on port {args.port}...")
        httpd.serve_forever()
except KeyboardInterrupt:
    print('Goodbye.')
