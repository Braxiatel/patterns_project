from zorro_framework.main import Framework
from zorro_framework.log_app import LogApplication
from zorro_framework.fake_app import FakeApplication
from urls import fronts
import argparse
from views import routes
from wsgiref.simple_server import make_server

parser = argparse.ArgumentParser(description='Simple implementation of web server.')
parser.add_argument("-p", "--port", help="Choose a port.", default=8000, type=int)
args = parser.parse_args()

application = Framework(routes, fronts)
log_app = LogApplication(routes, fronts)
fake_app = FakeApplication()


try:
    with make_server('', args.port, fake_app) as httpd:
        print(f"Running on port {args.port}...")
        httpd.serve_forever()
except KeyboardInterrupt:
    print('Goodbye.')
