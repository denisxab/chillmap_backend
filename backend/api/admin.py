from django.contrib import admin

from .models import GroupPlace, PlaceInMap, WhatTodo


@admin.register(WhatTodo)
class WhatTodoAdmin(admin.ModelAdmin):
    list_display = ("id", "todo")


@admin.register(GroupPlace)
class GroupPlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "img_url")


@admin.register(PlaceInMap)
class PlaceInMapAdmin(admin.ModelAdmin):
    list_display = ("id", "simpl_name", "cord_x", "cord_y", "rating", "address")
