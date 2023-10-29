import uuid
from django.db import models
from operation.models import BongoRestaurantBaseModel
from employee.models import Employee


class Restaurant(BongoRestaurantBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Menu(BongoRestaurantBaseModel):
    item_list = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_list


class Vote(BongoRestaurantBaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote_by = models.ForeignKey(Employee, on_delete=models.CASCADE)


class VoteResult(BongoRestaurantBaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    total_vote = models.IntegerField()
    date = models.DateField()
