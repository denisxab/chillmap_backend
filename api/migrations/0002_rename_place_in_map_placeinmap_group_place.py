# Generated by Django 4.2.1 on 2023-05-03 20:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="placeinmap",
            old_name="place_in_map",
            new_name="group_place",
        ),
    ]
