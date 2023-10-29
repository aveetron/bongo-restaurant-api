from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/auth/", include("employee.urls")),
    path("api/v1/restaurant/", include("restaurant.urls")),
    path("api/v1/operation/", include("operation.urls")),
]
