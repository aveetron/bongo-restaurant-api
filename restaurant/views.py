import logging
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from .serializers import RestaurantSerializer
from .models import Restaurant
from core.http_util import HttpUtil

logger = logging.getLogger(__name__)


class RestaurantAPIView(GenericAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            restaurants = Restaurant.objects.all()
            restaurant_serializer = RestaurantSerializer(restaurants,
                                                         many=True)
            return HttpUtil.success_response(
                "success",
                restaurant_serializer.data,
                status.HTTP_200_OK
            )
        except Exception as e:
            return HttpUtil.error_response(
                e.args[0],
                {},
                status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            payload = request.data
            if Restaurant.objects.filter(name=payload["name"]).exists():
                return HttpUtil.error_response(
                    "Restaurant with this name already exists!",
                    {},
                    status.HTTP_400_BAD_REQUEST
                )
            restaurant_serializer = RestaurantSerializer(data=payload)
            if restaurant_serializer.is_valid():
                restaurant_serializer.save(status=True)
                logger.info("restaurant created")
                return HttpUtil.success_response(
                    "restaurant created successfully!",
                    restaurant_serializer.data,
                    status.HTTP_201_CREATED
                )
            else:
                return HttpUtil.error_response(
                    restaurant_serializer.errors,
                    {},
                    status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return HttpUtil.error_response(
                e.args[0],
                {},
                status.HTTP_400_BAD_REQUEST
            )