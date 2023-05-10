# Generated by Django 4.2.1 on 2023-05-09 16:37

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ArialInMap",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        default=int,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор записи Int",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=254, verbose_name="Имя места расположения мест"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ареал места",
                "verbose_name_plural": "Ареал мест",
                "db_table": "arial_in_map",
            },
        ),
        migrations.CreateModel(
            name="ChannelGeomap",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        default=int,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор записи Int",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=254, verbose_name="Имя группы мест"),
                ),
                (
                    "shard",
                    models.SmallIntegerField(default=1, verbose_name="Номер шарда"),
                ),
                (
                    "arial_in_map",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="arial_in_map",
                        to="api.arialinmap",
                    ),
                ),
            ],
            options={
                "verbose_name": "Канал с местами",
                "verbose_name_plural": "Каналы с местами",
                "db_table": "channel_geomap",
            },
        ),
        migrations.CreateModel(
            name="TypePlace",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        default=int,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор записи Int",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="",
                        max_length=30,
                        verbose_name="Короткое имя предназначения группы",
                    ),
                ),
                (
                    "img_url",
                    models.CharField(
                        default="@/img/point.png", verbose_name="Путь к фото маркера"
                    ),
                ),
                (
                    "img_size_w",
                    models.FloatField(
                        default=0.3, verbose_name="Размер фото маркера W%"
                    ),
                ),
                (
                    "img_size_h",
                    models.FloatField(
                        default=0.3, verbose_name="Размер фото маркера H%"
                    ),
                ),
            ],
            options={
                "verbose_name": "Тип места",
                "verbose_name_plural": "Типы мест",
                "db_table": "type_place",
            },
        ),
        migrations.CreateModel(
            name="WhatTodo",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        default=int,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор записи Int",
                    ),
                ),
                ("todo", models.CharField(max_length=30)),
            ],
            options={
                "verbose_name": "Чем можно заняться в этом месте",
                "verbose_name_plural": "Чем можно заняться в этих местах",
                "db_table": "what_todo",
            },
        ),
        migrations.CreateModel(
            name="PlaceInMap",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор записи UUIDv4",
                    ),
                ),
                (
                    "simpl_name",
                    models.CharField(max_length=30, verbose_name="Короткое имя"),
                ),
                ("cord_x", models.CharField(max_length=20)),
                ("cord_y", models.CharField(max_length=20)),
                (
                    "rating",
                    models.SmallIntegerField(
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                        default=1,
                        verbose_name="Рейтинг места",
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        default="", max_length=255, verbose_name="Адрес места"
                    ),
                ),
                (
                    "channel_geomap",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="channel_geomap",
                        to="api.channelgeomap",
                    ),
                ),
                (
                    "type_place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="type_place",
                        to="api.typeplace",
                    ),
                ),
                (
                    "what_todo",
                    models.ManyToManyField(related_name="what_todo", to="api.whattodo"),
                ),
            ],
            options={
                "verbose_name": "Место",
                "verbose_name_plural": "Места",
                "db_table": "place_in_map",
                "unique_together": {("cord_x", "cord_y")},
            },
        ),
    ]
