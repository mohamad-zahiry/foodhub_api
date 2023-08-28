import os

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify

from PIL import Image


class Ingredient(models.Model):
    name = models.CharField(max_length=(50))


class Food(models.Model):
    class Category(models.TextChoices):
        FOOD = "F", _("Food")
        STARTER = "S", _("Starter")
        BEVERAGE = "B", _("Beverage")

    name = models.CharField(max_length=50)
    category = models.CharField(
        max_length=1, choices=Category.choices, default=Category.FOOD
    )
    ingredients = models.ManyToManyField(to="Ingredient")
    description = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(blank=True, null=True)
    is_in_menu = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        with Image.open(self.image.path) as img:
            os.remove(self.image.path)
            # set image width to 600 and fix height related to that
            c = 600 / img.width
            img = img.resize((round(img.width * c), round(img.height * c)))
            # create new name for image
            name = f"{self.pk}-{slugify(self.name)}.webp"

            img.save(settings.MEDIA_ROOT / name, "webp", optimize=True)
            self.image.name = name
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        os.remove(self.image.path)
        return super().delete(*args, **kwargs)


class Discount(models.Model):
    class DiscountType(models.TextChoices):
        FIXED = "F", _("Fixed price")
        PERCENTAGE = "P", _("Percentage")

    food = models.ForeignKey(to="Food", on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=1, choices=DiscountType.choices)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()

    def is_expired(self):
        return self.start_date + self.duration < timezone.now()
