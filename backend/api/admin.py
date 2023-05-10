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
    list_display = ("id", "simpl_name", "cord_x", "cord_y", "rating", "channel_geomap")
    ordering = ("channel_geomap", "simpl_name")


@admin.register(ChannelGeomap)
class ChannelGeomapAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "shard")


@admin.register(ArialInMap)
class ArialInMapAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
