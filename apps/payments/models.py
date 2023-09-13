from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    class State(models.IntegerChoices):
        NOT_PAID = 0, _("not paid")
        PAID = 1, _("Paid but not verified")
        VERIFIED = 2, _("paid and verified")

    user = models.ForeignKey("accounts.User", on_delete=models.DO_NOTHING)
    order_uuid = models.UUIDField()
    # after each payment(PAID state), foodhub send a verification request to
    # IDPay-api with "payment_id" of the transaction, if verified by IDPay-api,
    # the "state" change to VERIFIED.
    state = models.IntegerField(choices=State.choices, default=State.NOT_PAID)

    # these two fields generate by IDPay-api endpoint before payment
    payment_id = models.CharField(max_length=128)
    payment_link = models.URLField(max_length=512)

    # next fields are returned by IDPay-api endpoint after
    # doing transaction in PAID state
    idpay_status = models.IntegerField(default=0)
    idpay_track_id = models.IntegerField(default=0)
    idpay_order_id = models.CharField(max_length=50)
    idpay_card_no = models.CharField(max_length=20)
    idpay_hashed_card_no = models.CharField(max_length=64)
    idpay_date = models.DateTimeField(default=timezone.now)
