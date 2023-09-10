from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField


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
    class Status(models.TextChoices):
        IN_CART = "I", _("In cart")
        WAIT_FOR_COOK = "W", _("Waiting for cooking")
        COOKING = "C", _("Cooking")
        BOXING = "B", _("Boxing")
        ON_WAY = "O", _("On the way")
        ARRIVED = "A", _("Arrived")

    order_items = models.ManyToManyField(to="OrderItem")
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.IN_CART)

    def set_next_status(self):
        if not self.order_items.exists():
            raise ValidationError("you can't change status of an empty order")

        if self.status == self.Status.ARRIVED:
            return

        next_status = {
            self.Status.IN_CART: self.Status.WAIT_FOR_COOK,
            self.Status.WAIT_FOR_COOK: self.Status.COOKING,
            self.Status.COOKING: self.Status.BOXING,
            self.Status.BOXING: self.Status.ON_WAY,
            self.Status.ON_WAY: self.Status.ARRIVED,
        }
        self.status = next_status[self.status]
        self.save()


class DoneOrder(OrderAbstract):
    order_items = models.ManyToManyField(to="DoneOrderItem")
