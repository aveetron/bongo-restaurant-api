from rest_framework.serializers import ModelSerializer
from .models import Restaurant, Menu


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(ModelSerializer):

    class Meta:
        model = Menu
        fields = "__all__"