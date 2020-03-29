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


# broker details in the case of redis
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


"""
broker details in the case of rabbitmq
transport://userid:password@hostname:port/virtual_host
for rabbitmq, transport is amqp


"""
CELERY_BROKER_URL = 'amqp://guest:guest@localhost'
CELERY_RESULT_BACKEND = 'rpc://'


