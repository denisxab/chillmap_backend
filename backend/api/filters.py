from api.models.geomap import PlaceInMap
from django_filters import rest_framework as filters


class PlaceInMapFilter(filters.FilterSet):
    rating_gte = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    rating_lte = filters.NumberFilter(field_name="rating", lookup_expr="lte")
    rating_exact = filters.NumberFilter(field_name="rating", lookup_expr="exact")

    class Meta:
        model = PlaceInMap
        fields = ("simpl_name", "what_todo", "type_place", "channel_geomap")
