# Generated by Django 4.2.4 on 2023-08-21 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("foods", "0001_initial"),
        ("loyalty_club", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("discount", models.FloatField()),
                (
                    "food",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="foods.food"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoneOrderItem",
            fields=[
                (
                    "orderitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="orders.orderitem",
                    ),
                ),
            ],
            bases=("orders.orderitem",),
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("final_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("address", models.CharField(max_length=200)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("I", "In cart"),
                            ("W", "Waiting for cooking"),
                            ("C", "Cooking"),
                            ("B", "Boxing"),
                            ("O", "On the way"),
                            ("A", "Arrived"),
                        ],
                        default="I",
                        max_length=1,
                    ),
                ),
                (
                    "coupon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="loyalty_club.coupon",
                    ),
                ),
                ("order_items", models.ManyToManyField(to="orders.orderitem")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DoneOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("final_price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("address", models.CharField(max_length=200)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None
                    ),
                ),
                (
                    "coupon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="loyalty_club.coupon",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("order_items", models.ManyToManyField(to="orders.doneorderitem")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
