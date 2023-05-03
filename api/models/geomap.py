import uuid
from typing import Type

from django.contrib.gis.db import models
from django.db.models.manager import BaseManager


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name="Идентификатор записи",
        editable=True,
    )

    class Meta:
        abstract = True


class WhatTodo(BaseModel):
    """Чем можно заняться в этом месте на карте"""

    todo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Чем можно заняться в этом месте на карте"
        verbose_name_plural = "Чем можно заняться в этих местах на карте"
        db_table = "what_todo"

    def __str__(self) -> str:
        return self.todo


class GroupPlace(BaseModel):
    """Группа мест на карте"""

    name = models.CharField("Короткое группы", max_length=30, default="")

    class Meta:
        verbose_name = "Группа мест на карте"
        verbose_name_plural = "Группы мест на карте"
        db_table = "group_place"

    def __str__(self) -> str:
        return self.name


class PlaceInMap(BaseModel):
    """
    Место на карте
    """

    cord_x = models.CharField(max_length=18)
    cord_y = models.CharField(max_length=18)

    simpl_name = models.CharField("Короткое имя", max_length=30, default="")
    rating = models.SmallIntegerField(
        "Рейтинг места",
        default=1,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )
    address = models.CharField("Адрес места", max_length=255, default="")
    what_todo = models.ForeignKey(
        to=WhatTodo,
        related_name="what_todo",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    group_place = models.ManyToManyField(
        to=GroupPlace,
        related_name="group_place",
        blank=True,
    )

    class Meta:
        verbose_name = "Место на карте"
        verbose_name_plural = "Места на карте"
        db_table = "place_in_map"
        unique_together = ("cord_x", "cord_y")

    def __str__(self) -> str:
        return f"{self.simpl_name}: {self.cord_x},{self.cord_y}"
