from django.utils.timezone import timedelta
from .base import *


SECRET_KEY = get_config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "https://yourdomain.com",
    "*",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": get_config("DB_NAME"),
        "USER": get_config("DB_USER"),
        "PASSWORD": get_config("DB_PASS"),
        "HOST": get_config("DB_HOST"),
        "PORT": get_config("DB_PORT"),
    }
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=get_config("ACCESS_TOKEN_LIFETIME_in_minute")),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=get_config("REFRESH_TOKEN_LIFETIME_in_minute")),
}

IDPAY_API_KEY = get_config("IDPAY_API_KEY")
IDPAY_CALLBACK_URL = get_config("IDPAY_CALLBACK_URL")
IDPAY_SANDBOX_MODE = get_config("IDPAY_SANDBOX_MODE")
