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
    id = models.AutoField(
        primary_key=True,
        verbose_name="Идентификатор записи",
        editable=True,
    )

    class Meta:
        abstract = True
