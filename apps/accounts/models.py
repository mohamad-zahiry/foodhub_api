from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    name = models.CharField(max_length=128)
    phone = PhoneNumberField(unique=True)
    email = models.EmailField()
    coupons = models.ManyToManyField(to="loyalty_club.Coupon")

    USERNAME_FIELD = "phone"


class Address(models.Model):
    user = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
