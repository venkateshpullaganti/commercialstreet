from .commons import *


DEBUG = True

SECRET_KEY = 'django-insecure-(l4x)1*&bb75121)!ou5q=a7-3=j19-%3wqy&a!r^6)8h&^a^='



# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "commercialstreet",
        'USER':'root',
        'HOST':'mysql',
        'PASSWORD':'admin123',
        'PORT': '3306',
    }   
}


CELERY_BROKER_URL = 'redis://redis:6379/1'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'smtp4dev'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525



DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':lambda response:True
}