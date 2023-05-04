from rest_framework import routers

from .views import (
    ArialInMapViewSet,
    GroupPlaceViewSet,
    MetaGeomViewSet,
    PlaceInMapViewSet,
    WhatTodoViewSet,
)

router = routers.DefaultRouter()
router.register(r"place", PlaceInMapViewSet, basename="place")
router.register(r"what_todo", WhatTodoViewSet, basename="what_todo")
router.register(r"group_place", GroupPlaceViewSet, basename="group_place")
router.register(r"arial_in_map", ArialInMapViewSet, basename="arial_in_map")
router.register(r"meta_geomap", MetaGeomViewSet, basename="meta_geomap")


urlpatterns = router.urls
