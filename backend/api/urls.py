from rest_framework import routers

from .views import (
    ArialInMapViewSet,
    ChannelGeomapListPlaceViewSet,
    ChannelGeomapViewSet,
    PlaceInMapViewSet,
    TypePlaceViewSet,
    WhatTodoViewSet,
)

router = routers.DefaultRouter()
router.register(r"place", PlaceInMapViewSet, basename="place")
router.register(r"what_todo", WhatTodoViewSet, basename="what_todo")
router.register(r"type_place", TypePlaceViewSet, basename="type_place")
router.register(r"arial_in_map", ArialInMapViewSet, basename="arial_in_map")
router.register(r"channel_geomap", ChannelGeomapViewSet, basename="channel_geomap")
router.register(
    r"channel_geomap_place",
    ChannelGeomapListPlaceViewSet,
    basename="channel_geomap_place",
)


urlpatterns = router.urls
