
from django.contrib import admin

from .models import GroupPlace, PlaceInMap, WhatTodo


@admin.register(WhatTodo)
class WhatTodoAdmin(admin.ModelAdmin):
    ...


@admin.register(GroupPlace)
class GroupPlaceAdmin(admin.ModelAdmin):
    ...


@admin.register(PlaceInMap)
class PlaceInMapAdmin(admin.ModelAdmin):
    ...
