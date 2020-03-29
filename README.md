To monitor in webui on celery tasks

flower -A app.client --port=5555 

then go to 127.0.0.1:5555

** run celery worker to handle background tasks ** 
celery -A app.client worker -l info -P gevent --concurrency=2

** run python flask app ** 
python app.py

we should be running redis server and redis-cli client so that redis helps celery in communicating between celery and its workers



# Note
1)  please visit this link :
https://myaccount.google.com/lesssecureapps?pli=1


to turn off the security feature for the google account being used in this project for mailing feature.

2) this project also contains celery broker URLs for keeping rabbimq as borker instead of redis
(however, instaling rabbitmq is not in the readme.md file)

# Need to improve
1) Authentication/login mechanism with sessions
2) Portfolio to manage historical notifiers