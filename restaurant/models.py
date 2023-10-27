import uuid
from django.db import models
from operation.models import BongoRestaurantBaseModel


class Restaurant(BongoRestaurantBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name