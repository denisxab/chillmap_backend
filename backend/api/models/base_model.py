import uuid

from django.db import models


class ModelUUID(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        verbose_name="Идентификатор записи UUIDv4",
        editable=False,
    )

    class Meta:
        abstract = True


class ModelInteger(models.Model):
    id = models.IntegerField(
        primary_key=True,
        default=int,
        verbose_name="Идентификатор записи Int",
        editable=False,
    )

    class Meta:
        abstract = True
