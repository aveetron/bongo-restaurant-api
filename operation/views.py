from datetime import datetime, time, timedelta

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView

from core.http_util import HttpUtil
from restaurant.serializers import *

from .serializers import CurrentDayMenuSerializer


class CurrentDayMenuAPIView(GenericAPIView):
    serializer_class = CurrentDayMenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            today = datetime.now().date()
            tomorrow = today + timedelta(1)
            today_start = datetime.combine(today, time())
            today_end = datetime.combine(tomorrow, time())
            todays_menu = Menu.objects.filter(
                created_at__lte=today_end, created_at__gte=today_start
            )
            todays_menu_serializer = self.serializer_class(todays_menu, many=True)
            return HttpUtil.success_response(
                "success", todays_menu_serializer.data, status.HTTP_200_OK
            )
        except Exception as e:
            return HttpUtil.error_response(e.args[0], {}, status.HTTP_400_BAD_REQUEST)
