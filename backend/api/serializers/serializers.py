from api.models.geomap import (ArialInMap, ChannelGeomap, PlaceInMap,
                               TypePlace, WhatTodo)
from django.urls import reverse
from rest_framework import serializers


class MixinUrl(serializers.Serializer):
    self_url = serializers.SerializerMethodField(label="Ссылка на текущий объект.")

    class Meta:
        fields = ("self_url",)

    def get_self_url(self, obj):
        request = self.context.get("request")
        url = reverse(f"{self.Meta.url}-detail", kwargs={"pk": obj.pk})
        return request.build_absolute_uri(url)


class MixinUUIDv4(serializers.Serializer):
    id = serializers.UUIDField(read_only=True, label="Идентификатор записи UUIDv4.")

    class Meta:
        fields = ("id",)


class MixinInteger(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, label="Идентификатор записи Int.")

    class Meta:
        fields = ("id",)


class WhatTodoSerializers(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели WhatTodo"""

    class Meta:
        model = WhatTodo
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "todo",
        )
        url = "what_todo"


class TypePlaceSerializers(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели TypePlace"""

    class Meta:
        model = TypePlace
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "name",
            "img_url",
            "img_size_w",
            "img_size_h",
        )
        url = "type_place"


class ArialInMapSerializers(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели ArialInMap"""

    class Meta:
        model = ArialInMap
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "name",
        )
        url = "arial_in_map"


class ChannelGeomapSerializers(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели  ChannelGeomap"""

    arial_in_map_obj = ArialInMapSerializers(source="arial_in_map", read_only=True)

    class Meta:
        model = ChannelGeomap
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "name",
            "arial_in_map",
            "arial_in_map_obj",
            "shard",
        )
        url = "channel_geomap"


class PlaceInMapSerializers(MixinUUIDv4, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели PlaceInMap"""

    what_todo_obj = WhatTodoSerializers(source="what_todo", read_only=True, many=True)
    type_place_obj = TypePlaceSerializers(source="type_place", read_only=True)
    channel_geomap_obj = ChannelGeomapSerializers(
        source="channel_geomap", read_only=True
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
            "channel_geomap",
            "channel_geomap_obj",
            "what_todo",
            "what_todo_obj",
            "type_place",
            "type_place_obj",
        )
        url = "place"
