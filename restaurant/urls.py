from restaurant.views import *
from django.urls import path

urlpatterns = [
    path("", RestaurantAPIView.as_view()),
    path("menu/", MenuAPIView.as_view()),
]