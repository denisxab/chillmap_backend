from django.urls import reverse
from rest_framework import serializers

from api.models.geomap import ArialInMap, GroupPlace, MetaGeom, PlaceInMap, WhatTodo


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


class GroupPlaceSerializers(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели GroupPlace"""

    class Meta:
        model = GroupPlace
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "name",
        )
        url = "group_place"


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


class MetaGeomSerializers(MixinInteger, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели  MetaGeom"""

    arial_in_map_obj = ArialInMapSerializers(source="arial_in_map", read_only=True)

    class Meta:
        model = MetaGeom
        fields = (
            *MixinInteger.Meta.fields,
            *MixinUrl.Meta.fields,
            "name",
            "arial_in_map",
            "arial_in_map_obj",
            "shard",
        )
        url = "meta_geomap"


class PlaceInMapSerializers(MixinUUIDv4, MixinUrl, serializers.ModelSerializer):
    """Сериализация модели PlaceInMap"""

    what_todo_obj = WhatTodoSerializers(source="what_todo", read_only=True)
    group_place_obj = GroupPlaceSerializers(
        source="group_place", read_only=True, many=True
    )

    meta_geomap_obj = MetaGeomSerializers(source="meta_geomap", read_only=True)

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
            "meta_geomap",
            "meta_geomap_obj",
            "what_todo",
            "what_todo_obj",
            "group_place",
            "group_place_obj",
        )
        url = "place"
