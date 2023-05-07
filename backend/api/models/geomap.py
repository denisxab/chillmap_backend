import uuid

from django.db import models


class ModelUUID(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name="Идентификатор записи UUIDv4",
        editable=False,
    )

    class Meta:
        abstract = True


class ModelInteger(models.Model):
    id = models.IntegerField(
        primary_key=True,
        default=int,
        verbose_name="Идентификатор записи Int",
        editable=False,
    )

    class Meta:
        abstract = True


class WhatTodo(ModelInteger):
    """Чем можно заняться в этом месте на карте"""

    todo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Чем можно заняться в этом месте"
        verbose_name_plural = "Чем можно заняться в этих местах"
        db_table = "what_todo"

    def __str__(self) -> str:
        return self.todo


class GroupPlace(ModelInteger):
    """Группа предназначения мест на карте"""

    name = models.CharField(
        "Короткое имя предназначения группы", max_length=30, default=""
    )
    img_url = models.CharField("Путь к фото маркера", default="@/img/point.png")
    img_size_w = models.FloatField("Размер фото маркера W%", default=0.3)
    img_size_h = models.FloatField("Размер фото маркера H%", default=0.3)

    class Meta:
        verbose_name = "Группа предназначения места"
        verbose_name_plural = "Группы предназначения мест"
        db_table = "group_place"

    def __str__(self) -> str:
        return self.name


class ArialInMap(ModelInteger):
    """Справочник места расположения"""

    name = models.CharField("Имя места расположения мест", max_length=254)

    class Meta:
        verbose_name = "Справочник места расположения"
        verbose_name_plural = "Справочник мест расположения"
        db_table = "arial_in_map"

    def __str__(self) -> str:
        return self.name


class MetaGeom(ModelInteger):
    """Мета информация о месте"""

    name = models.CharField("Имя группы мест", max_length=254)
    arial_in_map = models.ForeignKey(
        to=ArialInMap, related_name="arial_in_map", on_delete=models.PROTECT
    )
    shard = models.SmallIntegerField("Номер шарда", default=1)

    class Meta:
        verbose_name = "Мета информация о месте"
        verbose_name_plural = "Мета информация о местах"
        db_table = "meta_geomap"

    def __str__(self) -> str:
        return self.name


class PlaceInMap(ModelUUID):
    """
    Место на карте
    """

    simpl_name = models.CharField("Короткое имя", max_length=30)

    cord_x = models.CharField(max_length=20)
    cord_y = models.CharField(max_length=20)

    rating = models.SmallIntegerField(
        "Рейтинг места",
        default=1,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )
    address = models.CharField("Адрес места", max_length=255, default="")
    meta_geomap = models.ForeignKey(
        to=MetaGeom,
        related_name="meta_geomap",
        on_delete=models.PROTECT,
        blank=True,
    )
    what_todo = models.ManyToManyField(
        to=WhatTodo,
        related_name="what_todo",
        blank=True,
    )
    group_place = models.ForeignKey(
        to=GroupPlace,
        related_name="group_place",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        db_table = "place_in_map"
        unique_together = ("cord_x", "cord_y")

    def __str__(self) -> str:
        return f"{self.simpl_name}: {self.cord_x},{self.cord_y}"
