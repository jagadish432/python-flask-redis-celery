# contains configurations for this project
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

SECRET_KEY = 'ILovePython'
HASH_SECRET = 'This is  my secret hash key'

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'maheshbabu4329@gmail.com'
MAIL_PASSWORD = '9030648036'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'



