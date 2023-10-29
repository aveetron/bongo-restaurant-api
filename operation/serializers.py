from rest_framework import serializers
from restaurant.models import Vote
from restaurant.serializers import VoteSerializer


class CurrentDayMenuSerializer(serializers.Serializer):
    guid = serializers.UUIDField(required=True)
    restaurant = serializers.CharField(required=True, source="restaurant.name")
    menu = serializers.CharField(required=True, source="item_list")
    total_vote = serializers.SerializerMethodField()
    date_time = serializers.DateTimeField(source="created_at")

    def get_total_vote(self, menu):
        votes = Vote.objects.filter(menu=menu)
        vote_list = [{"vote_by": vote.vote_by.email} for vote in votes]
        return vote_list


