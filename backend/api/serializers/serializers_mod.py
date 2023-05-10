from api.models.geomap import ChannelGeomap, PlaceInMap, TypePlace
from rest_framework import serializers

from .serializers import (ArialInMapSerializers, MixinInteger, MixinUrl,
                          MixinUUIDv4, WhatTodoSerializers)


class DPlaceInMapSerializers(MixinUUIDv4, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели PlaceInMap который используется в  ChannelGeomapListPlace"""

    what_todo_obj = WhatTodoSerializers(source="what_todo", read_only=True, many=True)

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


class ChannelGeomapListPlace(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели  ChannelGeomap в которой отобразиться список мест
    которые входят в этот канал
    """

    arial_in_map_obj = ArialInMapSerializers(source="arial_in_map", read_only=True)
    places = serializers.SerializerMethodField(read_only=True)

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

    def get_places(self, obj):
        return ""

    def to_representation(self, instance):
        # Вызываем родительский метод to_representation()
        res = super().to_representation(instance)

        places = DPlaceInMapSerializers(
            instance.channel_geomap.all(), many=True, context=self.context
        ).data
        # Создаем пустой словарь type_place_dict для группировки мест по
        # типу места
        type_place_dict = dict()

        # Проходимся по списку мест и добавляем их ID в словарь
        # type_place_dict, сгруппированный по типу места
        for p in places:
            if t := type_place_dict.get(p["type_place"]):
                t.append(p)
            else:
                type_place_dict[p["type_place"]] = [p]

        # Для каждого типа места из базы данных TypePlace, заменяем его ID
        # на его имя в словаре type_place_dict
        for r in TypePlace.objects.filter(pk__in=tuple(type_place_dict.keys())):
            type_place_dict[r.name] = type_place_dict.pop(r.pk)

        res["places"] = type_place_dict
        # Возвращаем измененный словарь представления объекта модели
        return res
