DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lolaws',
        'USER': 'lolaws',
        'PASSWORD': 'SETME', # Exercise 2
        'HOST': 'SETME', # Exercise 2
        'PORT': '',
    }
}

AWS_ACCESS_KEY_ID = "SETME"
AWS_SECRET_ACCESS_KEY = "SETME"
AWS_STORAGE_BUCKET_NAME = "SETME"

# S3 - Exercise 3
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'

#STATIC_URL = 'http://'+AWS_STORAGE_BUCKET_NAME+'.s3.amazonaws.com/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

AWS_HEADERS = {
    'Cache-Control': 'max-age=86400',
}

from S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

# email
EMAIL_BACKEND = 'django_ses.SESBackend'
DEFAULT_FROM_EMAIL = 'lolaws <SETME@EMAIL.LOL>'
EMAIL_SUBJECT_PREFIX = '[lolaws] '
