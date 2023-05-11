from collections import defaultdict
from api.models.geomap import ChannelGeomap, PlaceInMap, TypePlace
from rest_framework import serializers

from .serializers import (
    ArialInMapSerializers,
    MixinInteger,
    MixinUrl,
    MixinUUIDv4,
    TypePlaceSerializers,
    WhatTodoSerializers,
)


class DPlaceInMapSerializers(
    MixinUUIDv4,
    MixinUrl,
    serializers.ModelSerializer,
):
    """Сериализация модели PlaceInMap который используется
    в  ChannelGeomapListPlace"""

    what_todo_obj = WhatTodoSerializers(
        source="what_todo",
        read_only=True,
        many=True,
    )

    class Meta:
        model = PlaceInMap
        fields = (
            *MixinUUIDv4.Meta.fields,
            *MixinUrl.Meta.fields,
            "cord_x",
            "cord_y",
            "simpl_name",
            "rating",
            "address",
            "what_todo_obj",
            "type_place",
        )
        url = "place"


class PlacesSerializers(serializers.Serializer):
    place = serializers.SerializerMethodField(read_only=True)

    def get_place(self, obj):
        ...

    def to_representation(self, instance):
        res = super().to_representation(instance)

        places = DPlaceInMapSerializers(
            instance.all(), many=True, context=self.context
        ).data

        # Группировка мест по типу места с использованием defaultdict
        place = defaultdict(list)
        for p in places:
            p_type = p.get("type_place", None)
            if p_type is not None:
                place[p_type].append(p)

        # Получение всех идентификаторов типов мест
        type_place_ids = place.keys()

        # Запрос всех объектов TypePlace за один раз
        type_places = TypePlace.objects.filter(pk__in=type_place_ids)
        type_places_data = TypePlaceSerializers(
            type_places, many=True, context=self.context
        ).data

        # Создание словаря настроек, где ключ - идентификатор типа места
        # , а значение - данные TypePlace
        settings = {tp["id"]: tp for tp in type_places_data}

        res["settings"] = settings
        # Преобразование defaultdict в обычный словарь
        res["place"] = dict(place)

        return res


class ChannelGeomapListPlaceSerializers(
    MixinInteger, MixinUrl, serializers.ModelSerializer
):
    """Сериализация модели  ChannelGeomap в которой отобразиться список мест
    которые входят в этот канал
    """

    arial_in_map_obj = ArialInMapSerializers(
        source="arial_in_map",
        read_only=True,
    )
    places = PlacesSerializers(source="channel_geomap", read_only=True)

    class Meta:
        model = ChannelGeomap
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "name",
            "arial_in_map",
            "arial_in_map_obj",
            "shard",
            "places",
        )
        url = "channel_geomap_place"
