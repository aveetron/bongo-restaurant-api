from django.urls import path

from operation.views import *

urlpatterns = [
    path("todays-menu", CurrentDayMenuAPIView.as_view()),
]
