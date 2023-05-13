from api.utils import get_address_from_coord
from conf.settings import logger_api
from django.db import models

from .base_model import ModelInteger, ModelUUID


class WhatTodo(ModelInteger):
    """Чем можно заняться в этом месте на карте"""

    todo = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Чем можно заняться в этом месте"
        verbose_name_plural = "Чем можно заняться в этих местах"
        db_table = "what_todo"

    def __str__(self) -> str:
        return self.todo


class TypePlace(ModelInteger):
    """Типы мест"""

    name = models.CharField(
        "Короткое имя предназначения группы", max_length=30, default=""
    )
    img_url = models.CharField("Путь к фото маркера", default="@/img/point.png")
    img_size_w = models.FloatField("Размер фото маркера W%", default=0.3)
    img_size_h = models.FloatField("Размер фото маркера H%", default=0.3)

    class Meta:
        verbose_name = "Тип места"
        verbose_name_plural = "Типы мест"
        db_table = "type_place"

    def __str__(self) -> str:
        return self.name


class ArialInMap(ModelInteger):
    """Ареал мест"""

    name = models.CharField("Имя места расположения мест", max_length=254)

    class Meta:
        verbose_name = "Ареал места"
        verbose_name_plural = "Ареал мест"
        db_table = "arial_in_map"

    def __str__(self) -> str:
        return self.name


class ChannelGeomap(ModelInteger):
    """Каналы с местами"""

    name = models.CharField("Имя группы мест", max_length=254)
    arial_in_map = models.ForeignKey(
        to=ArialInMap, related_name="arial_in_map", on_delete=models.PROTECT
    )
    shard = models.SmallIntegerField("Номер шарда", default=1)

    class Meta:
        verbose_name = "Канал с местами"
        verbose_name_plural = "Каналы с местами"
        db_table = "channel_geomap"

    def __str__(self) -> str:
        return self.name


class PlaceInMap(ModelUUID):
    """Место на карте"""

    simpl_name = models.CharField("Короткое имя", max_length=30)

    cord_x = models.CharField(max_length=20)
    cord_y = models.CharField(max_length=20)

    rating = models.SmallIntegerField(
        "Рейтинг места",
        default=1,
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )
    address = models.CharField("Адрес места", max_length=255, default="", blank=True)
    channel_geomap = models.ForeignKey(
        to=ChannelGeomap,
        related_name="channel_geomap",
        on_delete=models.PROTECT,
    )
    what_todo = models.ManyToManyField(
        to=WhatTodo,
        related_name="what_todo",
    )
    type_place = models.ForeignKey(
        to=TypePlace,
        related_name="type_place",
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        db_table = "place_in_map"
        unique_together = ("cord_x", "cord_y")

    def __str__(self) -> str:
        return f"{self.simpl_name}: {self.cord_x},{self.cord_y}"

    def save(self, *args, **kwargs):
        # Если не указан адрес, то тогда пытаемся найти адрес автоматически
        # если, автоматически не получается, то берем координаты
        if not self.address:
            new_address: tuple[bool, str] = get_address_from_coord(
                self.cord_x, self.cord_y
            )
            if new_address[0]:
                self.address = new_address[1]
            else:
                self.address = f"{self.cord_x},{self.cord_y}"
                print(f"Ошибка при получении адреса: '{self.address}'")
        super().save(*args, **kwargs)
        logger_api.info(f"Успешно создано нового места: {self}")

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        logger_api.info(f"Успешно удаление места: {self}")
        return res
