from .base import *


SECRET_KEY = "django-insecure-x+wc7i=$ny*tg_6p31f74b(68f*wte*=cdpw=0alelrvktf7$m"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "foodhub",
        "USER": "foodhub_user",
        "PASSWORD": "1234",
        "HOST": "172.17.0.2",
        "PORT": 3306,
    }
}

PHONENUMBER_DEFAULT_REGION = "IR"
