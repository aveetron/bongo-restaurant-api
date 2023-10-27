from django.db import models
import uuid


class BongoRestaurantBaseModel(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        abstract = True
