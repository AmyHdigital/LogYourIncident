from incidentApp.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'incidents',
        'USER': 'newuser',
        'PASSWORD': 'password',
        'HOST': 'localhost'
    }
}