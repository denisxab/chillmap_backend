from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from api.models.geomap import GroupPlace, PlaceInMap, WhatTodo
from api.pagination import PointPagination
from api.serializers import (
    GroupPlaceSerializers,
    PlaceInMapSerializers,
    WhatTodoSerializers,
)


class PlaceInMapViewSet(ModelViewSet):
    queryset = (
        PlaceInMap.objects.all()
        .select_related("what_todo")
        .prefetch_related("group_place")
    )
    serializer_class = PlaceInMapSerializers
    pagination_class = PointPagination


class WhatTodoViewSet(ModelViewSet):
    queryset = WhatTodo.objects.all()
    serializer_class = WhatTodoSerializers
    pagination_class = PointPagination


class GroupPlaceViewSet(ModelViewSet):
    queryset = GroupPlace.objects.all()
    serializer_class = GroupPlaceSerializers
    pagination_class = PointPagination
