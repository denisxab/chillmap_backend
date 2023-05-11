# Generated by Django 4.2.1 on 2023-05-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="arialinmap",
            name="id",
            field=models.IntegerField(
                default=int,
                primary_key=True,
                serialize=False,
                verbose_name="Идентификатор записи Int",
            ),
        ),
        migrations.AlterField(
            model_name="channelgeomap",
            name="id",
            field=models.IntegerField(
                default=int,
                primary_key=True,
                serialize=False,
                verbose_name="Идентификатор записи Int",
            ),
        ),
        migrations.AlterField(
            model_name="placeinmap",
            name="address",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="Адрес места"
            ),
        ),
        migrations.AlterField(
            model_name="typeplace",
            name="id",
            field=models.IntegerField(
                default=int,
                primary_key=True,
                serialize=False,
                verbose_name="Идентификатор записи Int",
            ),
        ),
        migrations.AlterField(
            model_name="whattodo",
            name="id",
            field=models.IntegerField(
                default=int,
                primary_key=True,
                serialize=False,
                verbose_name="Идентификатор записи Int",
            ),
        ),
    ]
