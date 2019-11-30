to monitor in webui on celery tasks
flower -A app.client --port=5555 
go to 127.0.0.1:5555

run celery worker to handle background tasks
celery -A app.client worker -l info -P gevent

run python flask app
python app.py

we should be using pipenv for this project to handle virtual environments

we should be running redis server and redis-cli client so that redis helps celery in communicating between celery and its workers


# Need to improve
1) Authentication/login mechanism with sessions
2) Portfolio to manage historical notifiers