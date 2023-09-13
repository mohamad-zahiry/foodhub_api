from uuid import uuid1

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField


def uuid():
    return uuid1().hex


class OrderItem(models.Model):
    food = models.ForeignKey(to="foods.Food", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.FloatField()
    user = models.ForeignKey(to="accounts.User", on_delete=models.DO_NOTHING)


class DoneOrderItem(OrderItem):
    pass


class OrderAbstract(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.DO_NOTHING)
    date = models.DateField(default=timezone.now)
    final_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    address = models.CharField(max_length=200, blank=True, default="")
    coupon = models.ForeignKey(to="loyalty_club.Coupon", on_delete=models.DO_NOTHING, null=True)
    phone = PhoneNumberField()

    class Meta:
        abstract = True


class Order(OrderAbstract):
    class State(models.IntegerChoices):
        ORDER = 0, _("Ordering")
        PAYMENT = 1, _("Awaiting payment")
        COOK = 2, _("Cooking")
        DELIVERY = 3, _("Delivering")

    uuid = models.UUIDField(auto_created=True, default=uuid, editable=False)
    order_items = models.ManyToManyField(to="OrderItem")
    state = models.IntegerField(choices=State.choices, default=State.ORDER)


class DoneOrder(OrderAbstract):
    uuid = models.UUIDField()
    order_items = models.ManyToManyField(to="DoneOrderItem")


class CanceledOrder(DoneOrderItem):
    order_items = models.JSONField()
    reason = models.CharField(max_length=200)
