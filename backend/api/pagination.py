from typing import Union

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PointPagination(PageNumberPagination):
    # Размер страницы по умолчанию
    page_size = 10
    # Имя параметра запроса для настройки размера страницы
    page_size_query_param = "page_size"
    # Максимальный размер страницы
    max_page_size = 1000

    # В этом примере мы переопределяем метод, в котором формируется страница
    def get_paginated_response(self, data: Union[dict, list]) -> Response:
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "count_pages": self.page.paginator.num_pages,
                "page_size": self.request.query_params.get(
                    self.page_size_query_param, self.page_size
                ),
                "current_page": self.page.number,
                "results": data,
            }
        )
