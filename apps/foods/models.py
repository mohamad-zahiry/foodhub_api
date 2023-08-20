from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(max_length=(50))


class Food(models.Model):
    name = models.CharField(max_length=50)
    ingredients = models.ManyToManyField(to="Ingredient")
    description = models.CharField(max_length=500, blank=True)
    is_in_menu = models.BooleanField(default=True)


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        FIXED = "F", _("Fixed price")
        PERCENTAGE = "P", _("Percentage")

    food = models.ForeignKey(to="Food", on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=1, choices=DiscountType.choices)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()
