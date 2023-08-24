from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group

from phonenumber_field.modelfields import PhoneNumberField

from apps.constants import GROUPS


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email, and password"""
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=128)
    phone = PhoneNumberField()
    coupons = models.ManyToManyField(to="loyalty_club.Coupon")
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        default_group = Group.objects.get(name=GROUPS.CUSTOMER)
        super().save(*args, **kwargs)
        if not self.groups.all().exists():
            self.groups.add(default_group)
        return super().save(*args, **kwargs)


class Address(models.Model):
    user = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
