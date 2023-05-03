from rest_framework import routers

from .views import GroupPlaceViewSet, PlaceInMapViewSet, WhatTodoViewSet

router = routers.DefaultRouter()
router.register(r"place", PlaceInMapViewSet, basename="place")
router.register(r"what_todo", WhatTodoViewSet, basename="what_todo")
router.register(r"group_place", GroupPlaceViewSet, basename="group_place")

urlpatterns = router.urls
