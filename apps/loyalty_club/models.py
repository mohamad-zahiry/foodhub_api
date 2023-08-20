from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


class LoyaltyClub(models.Model):
    user = models.OneToOneField(to="accounts.User", on_delete=models.CASCADE)
    join_date = models.DateField(default=timezone.now)
    score = models.IntegerField(default=0)


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        FIXED = "F", _("Fixed price")
        PERCENTAGE = "P", _("Percentage")

    class ForUsers(models.TextChoices):
        ALL = "AL", _("All users")
        JE = "JE", _("Join date Equal to y-m-d")
        JB = "JB", _("Join date Before y-m-d")
        JA = "JA", _("Join date After y-m-d")
        SE = "SE", _("Score Equal to n")
        SL = "SL", _("Score Less than n")
        SM = "SM", _("Score More than n")

    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    start_date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField()
    discount_type = models.CharField(max_length=1, choices=DiscountType.choices)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    for_users = models.CharField(max_length=2, choices=ForUsers.choices)
    score = models.IntegerField()
    join_date = models.DateField(default=timezone.now)
