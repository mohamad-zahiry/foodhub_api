from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    name = models.CharField(max_length=128)
    phone = PhoneNumberField()
    email = models.EmailField(unique=True)
    coupons = models.ManyToManyField(to="loyalty_club.Coupon")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Address(models.Model):
    user = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
