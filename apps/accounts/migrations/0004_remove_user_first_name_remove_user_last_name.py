# Generated by Django 4.2.4 on 2023-09-07 17:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_remove_user_first_name_remove_user_last_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
    ]