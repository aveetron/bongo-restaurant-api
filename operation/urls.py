from operation.views import *
from django.urls import path

urlpatterns = [
    path("todays-menu", CurrentDayMenuAPIView.as_view()),
]