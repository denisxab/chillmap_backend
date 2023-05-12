from api.filters import PlaceInMapFilter
from api.models.geomap import ArialInMap, ChannelGeomap, PlaceInMap, TypePlace, WhatTodo
from api.serializers import (
    ArialInMapSerializers,
    ChannelGeomapListPlaceSerializers,
    ChannelGeomapSerializers,
    PlaceInMapSerializers,
    TypePlaceSerializers,
    WhatTodoSerializers,
)
from django_filters import rest_framework as filters

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class PlaceInMapViewSet(ModelViewSet):
    queryset = (
        PlaceInMap.objects.all()
        .select_related("type_place", "channel_geomap")
        .prefetch_related("what_todo")
    )
    serializer_class = PlaceInMapSerializers
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlaceInMapFilter


class WhatTodoViewSet(ModelViewSet):
    queryset = WhatTodo.objects.all()
    serializer_class = WhatTodoSerializers


class TypePlaceViewSet(ModelViewSet):
    queryset = TypePlace.objects.all()
    serializer_class = TypePlaceSerializers


class ArialInMapViewSet(ModelViewSet):
    queryset = ArialInMap.objects.all()
    serializer_class = ArialInMapSerializers


class ChannelGeomapViewSet(ModelViewSet):
    queryset = ChannelGeomap.objects.all()
    serializer_class = ChannelGeomapSerializers


class ChannelGeomapListPlaceViewSet(ReadOnlyModelViewSet):
    queryset = ChannelGeomap.objects.all()
    serializer_class = ChannelGeomapListPlaceSerializers
