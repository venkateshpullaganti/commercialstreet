release: python manage.py migrate
web: gunicorn commercialstreet.wsgi
worker: celery -A commercialstreet worker