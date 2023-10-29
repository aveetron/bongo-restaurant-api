from restaurant.views import *
from django.urls import path

urlpatterns = [
    path("", RestaurantAPIView.as_view()),
    path("menu/", MenuAPIView.as_view()),
    path("menu/vote/<str:menu_guid>", VoteMenuDetailsAPIView.as_view()),
    path("vote-result", VoteResultAPIView.as_view()),
]