import uuid

from django.db import models


class BongoRestaurantBaseModel(models.Model):
    guid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True
