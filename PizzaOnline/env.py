import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV = os.environ.get('ENV', 'local').lower()


with open(os.path.join(BASE_DIR, 'PizzaOnline', 'build', 'env', '%s.json' % ENV.lower())) as data_file:
    environment_details = json.load(data_file)


def get_environment_details():
    return environment_details, ENV
# {
#   "DEBUG": "True",
#   "SECRET_KEY": "e=%52(gf@h(f0=l+%-1w6f(($*1^+qftns(vj4_d$5e!)nr_ct",
#   "ALLOWED_HOSTS": [
#     "*"
#   ],
#   "DATABASE": {
#     "NAME": "pizzadb",
#     "USER": "postgres",
# //    "PASSWORD": "mysecretpassword",
#     "PASSWORD": "postgres",
#     "HOST": "localhost",
# //    "HOST": "192.168.51.40",
#     "PORT": "5432"
# //    "PORT": "5433"
#   },
# //  "SITE_URL": "http://0.0.0.0:8000/",
#   "SITE_URL": "http://127.0.0.1:8000/",
#   "MEDIA_URL": "'/media/'",
#   "STATIC_URL": "'/static/'"
# }
#
