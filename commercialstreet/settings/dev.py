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
        'HOST':'localhost',
        'PASSWORD':'admin123',
        'PORT': '3306',
    }   
}

