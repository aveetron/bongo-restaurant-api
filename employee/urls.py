from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from employee.views import RegisterAPIView
from django.urls import path

urlpatterns = [
    path('registration/', RegisterAPIView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]