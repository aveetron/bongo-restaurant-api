from rest_framework.serializers import ModelSerializer
from .models import *


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class MenuSerializer(ModelSerializer):

    class Meta:
        model = Menu
        fields = "__all__"


class VoteSerializer(ModelSerializer):

    class Meta:
        model = Vote
        fields = ["menu"]


class VoteResultSerializer(ModelSerializer):

    class Meta:
        model = VoteResult
        fields = "__all__"