# Generated by Django 4.2.4 on 2023-09-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doneorder",
            name="uuid",
            field=models.UUIDField(unique=True),
        ),
    ]
