from django.urls import reverse
from rest_framework import serializers

from api.models.geomap import ArialInMap, GroupPlace, MetaGeom, PlaceInMap, WhatTodo


class BaseSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True, label="Идентификатор записи.")
    self_url = serializers.SerializerMethodField(label="Ссылка на текущий объект.")

    class Meta:
        model = GroupPlace
        fields = ("id", "self_url")

    def get_self_url(self, obj):
        request = self.context.get("request")
        url = reverse(f"{self.Meta.url}-detail", kwargs={"pk": obj.pk})
        return request.build_absolute_uri(url)


class WhatTodoSerializers(BaseSerializers):
    """Сериализация модели WhatTodo"""

    class Meta:
        model = WhatTodo
        fields = (
            *BaseSerializers.Meta.fields,
            "todo",
        )
        url = "what_todo"


class GroupPlaceSerializers(BaseSerializers):
    """Сериализация модели GroupPlace"""

    class Meta:
        model = GroupPlace
        fields = (
            *BaseSerializers.Meta.fields,
            "name",
        )
        url = "group_place"


class ArialInMapSerializers(BaseSerializers):
    """Сериализация модели ArialInMap"""

    class Meta:
        model = ArialInMap
        fields = (*BaseSerializers.Meta.fields, "name")
        url = "arial_in_map"


class MetaGeomSerializers(BaseSerializers):
    """Сериализация модели  MetaGeom"""

    arial_in_map_obj = ArialInMapSerializers(source="arial_in_map", read_only=True)

    class Meta:
        model = MetaGeom
        fields = (
            *BaseSerializers.Meta.fields,
            "name",
            "arial_in_map",
            "arial_in_map_obj",
            "shard",
        )
        url = "meta_geomap"


class PlaceInMapSerializers(BaseSerializers):
    """Сериализация модели PlaceInMap"""

    what_todo_obj = WhatTodoSerializers(source="what_todo", read_only=True)
    group_place_obj = GroupPlaceSerializers(
        source="group_place", read_only=True, many=True
    )

    meta_geomap_obj = MetaGeomSerializers(source="meta_geomap", read_only=True)

    class Meta:
        model = PlaceInMap
        fields = (
            *BaseSerializers.Meta.fields,
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
