from rest_framework.response import Response
from rest_framework.views import APIView

from .settings import SERVER_VERSION, logger_api
from .settings_local import (
    HOST_SRERVER_FRONT_DEV,
    HOST_SRERVER_FRONT_PROD,
    HOST_SRERVER_STATIC,
)


class GetUrlsView(APIView):
    """Показать спсиок хостов"""

    def get(self, request, *args, **kwargs):
        logger_api.info("Вызов: Get Urls")
        return Response(
            {
                # Хост для раздачи сатических файлов
                "HOST_SRERVER_STATIC": HOST_SRERVER_STATIC,
                # Хост для Django
                "HOST_SRERVER_BACKEND": request.build_absolute_uri().replace(
                    "get_url/", ""
                ),
                # Хост для Front
                "HOST_SRERVER_FRONT_DEV": HOST_SRERVER_FRONT_DEV,
                "HOST_SRERVER_FRONT_PROD": HOST_SRERVER_FRONT_PROD,
            }
        )


class AboutView(APIView):
    """Показать список хостов"""

    def get(self, request, *args, **kwargs):
        logger_api.info("Вызов: About")
        return Response({"version": SERVER_VERSION})
