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
