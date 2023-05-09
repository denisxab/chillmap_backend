from django.contrib import admin

from .models import ArialInMap, ChannelGeomap, PlaceInMap, TypePlace, WhatTodo


@admin.register(WhatTodo)
class WhatTodoAdmin(admin.ModelAdmin):
    list_display = ("id", "todo")


@admin.register(TypePlace)
class TypePlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "img_url")


@admin.register(PlaceInMap)
class PlaceInMapAdmin(admin.ModelAdmin):
    list_display = ("id", "simpl_name", "cord_x", "cord_y", "rating", "address")
    change_form_template = "admin/change_form.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        # extra_context["osm_data"] = self.get_dynamic_info()
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


@admin.register(ChannelGeomap)
class ChannelGeomapAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "shard")


@admin.register(ArialInMap)
class ArialInMapAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
