import uuid
from django.db import models
from operation.models import BongoRestaurantBaseModel


class Restaurant(BongoRestaurantBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(BongoRestaurantBaseModel):
    item_list = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_list