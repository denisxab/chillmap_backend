from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet

from api.filters import PlaceInMapFilter
from api.models.geomap import ArialInMap, GroupPlace, MetaGeom, PlaceInMap, WhatTodo
from api.pagination import PointPagination
from api.serializers import (
    ArialInMapSerializers,
    GroupPlaceSerializers,
    MetaGeomSerializers,
    PlaceInMapSerializers,
    WhatTodoSerializers,
)


class PlaceInMapViewSet(ModelViewSet):
    queryset = (
        PlaceInMap.objects.all()
        .select_related("what_todo", "meta_geomap")
        .prefetch_related("group_place")
    )
    serializer_class = PlaceInMapSerializers
    pagination_class = PointPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlaceInMapFilter


class WhatTodoViewSet(ModelViewSet):
    queryset = WhatTodo.objects.all()
    serializer_class = WhatTodoSerializers
    pagination_class = PointPagination


class GroupPlaceViewSet(ModelViewSet):
    queryset = GroupPlace.objects.all()
    serializer_class = GroupPlaceSerializers
    pagination_class = PointPagination


class ArialInMapViewSet(ModelViewSet):
    queryset = ArialInMap.objects.all()
    serializer_class = ArialInMapSerializers
    pagination_class = PointPagination


class MetaGeomViewSet(ModelViewSet):
    queryset = MetaGeom.objects.all()
    serializer_class = MetaGeomSerializers
    pagination_class = PointPagination
