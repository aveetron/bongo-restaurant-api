from restaurant.views import RestaurantAPIView
from django.urls import path

urlpatterns = [
    path("", RestaurantAPIView.as_view()),
]