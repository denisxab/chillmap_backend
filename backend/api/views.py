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
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from conf.settings_local import HOST_SRERVER_FRONT, HOST_SRERVER_STATIC


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


class GetUrls(APIView):
    """Показать спсиок хостов"""

    def get(self, request, *args, **kwargs):
        return Response(
            {
                # Хост для раздачи сатических файлов
                "HOST_SRERVER_STATIC": HOST_SRERVER_STATIC,
                # Хост для Django
                "HOST_SRERVER_BACKEND": request.build_absolute_uri().replace(
                    "get_url/", ""
                ),
                # Хост для Front
                "HOST_SRERVER_FRONT": HOST_SRERVER_FRONT,
            }
        )
