from zorro_framework.main import Framework
from zorro_framework.log_app import LogApplication
from zorro_framework.fake_app import FakeApplication
from urls import fronts
import argparse
from views import routes
from wsgiref.simple_server import make_server

parser = argparse.ArgumentParser(description='Simple implementation of web server.',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-p", "--port", help="Choose a port.", default=8000, type=int)
parser.add_argument("-a", "--application",
                    help="Choose an application to run: \n- 'main_app' to run Framework \n"
                         "- 'log_app' to run LoggingApplication \n- 'fake_app' to run FakeApplications",
                    default='main_app', type=str)
args = parser.parse_args()

application = Framework(routes, fronts)
log_app = LogApplication(routes, fronts)
fake_app = FakeApplication()

app_dict = {
    "main_app": application,
    "log_app": log_app,
    "fake_app": fake_app
}


try:
    with make_server('', args.port, app_dict[args.application]) as httpd:
        print(f"Running on port {args.port} for {app_dict[args.application]}...")
        httpd.serve_forever()
except KeyboardInterrupt:
    print('Goodbye.')
