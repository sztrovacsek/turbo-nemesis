web: gunicorn prandius.wsgi --log-file -
worker: celery worker --app=prandius.celery.app
