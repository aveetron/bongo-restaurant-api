import logging
from datetime import datetime, time, timedelta

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView

from core.http_util import HttpUtil

from .models import *
from .serializers import *

logger = logging.getLogger(__name__)


class RestaurantAPIView(GenericAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            restaurants = Restaurant.objects.all()
            restaurant_serializer = self.serializer_class(restaurants, many=True)
            return HttpUtil.success_response(
                "success", restaurant_serializer.data, status.HTTP_200_OK
            )
        except Exception as e:
            return HttpUtil.error_response(e.args[0], {}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            payload = request.data
            if Restaurant.objects.filter(name=payload["name"]).exists():
                return HttpUtil.error_response(
                    "Restaurant with this name already exists!",
                    {},
                    status.HTTP_400_BAD_REQUEST,
                )
            restaurant_serializer = self.serializer_class(data=payload)
            if restaurant_serializer.is_valid():
                restaurant_serializer.save(status=True)
                logger.info("restaurant created")
                return HttpUtil.success_response(
                    "restaurant created successfully!",
                    restaurant_serializer.data,
                    status.HTTP_201_CREATED,
                )
            else:
                return HttpUtil.error_response(
                    restaurant_serializer.errors, {}, status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return HttpUtil.error_response(e.args[0], {}, status.HTTP_400_BAD_REQUEST)


class MenuAPIView(GenericAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            menus = Menu.objects.all()
            menu_serializer = self.serializer_class(menus, many=True)
            return HttpUtil.success_response(
                "success", menu_serializer.data, status.HTTP_200_OK
            )
        except Exception as e:
            return HttpUtil.error_response(e.args[0], {}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            payload = request.data
            menu_serializer = self.serializer_class(data=payload)
            if menu_serializer.is_valid():
                menu_serializer.save(status=True)
                logger.info("restaurant created")
                return HttpUtil.success_response(
                    "restaurant created successfully!",
                    menu_serializer.data,
                    status.HTTP_201_CREATED,
                )
            else:
                return HttpUtil.error_response(
                    menu_serializer.errors, {}, status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return HttpUtil.error_response(e.args[0], {}, status.HTTP_400_BAD_REQUEST)


class VoteMenuDetailsAPIView(GenericAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, menu_guid):
        menu = Menu.objects.filter(guid=menu_guid).last()
        if not menu:
            return HttpUtil.error_response(
                "no menu exists!", {}, status.HTTP_400_BAD_REQUEST
            )

        """ check this user already voted or not """
        vote_by_the_user = Vote.objects.filter(menu=menu, vote_by=request.user)
        if vote_by_the_user.exists():
            return HttpUtil.error_response(
                "vote by this user already submitted", {}, status.HTTP_400_BAD_REQUEST
            )
        vote = Vote(menu=menu, vote_by=request.user)
        vote.save()
        return HttpUtil.success_response("created", {}, status.HTTP_201_CREATED)


class VoteResultAPIView(GenericAPIView):
    serializer_class = VoteResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        todays_menus = Menu.objects.filter(
            created_at__lte=today_end, created_at__gte=today_start
        )

        """ delete all previous votes """
        vote_results = VoteResult.objects.filter(
            created_at__lte=today_end, created_at__gte=today_start
        )
        vote_results.delete()

        for menu in todays_menus:
            total_menu_wise_vote = Vote.objects.filter(
                created_at__lte=today_end, created_at__gte=today_start, menu=menu
            ).count()

            vote_result = VoteResult(
                menu=menu, total_vote=total_menu_wise_vote, date=datetime.now().date()
            )
            vote_result.save()

        vote_results = VoteResult.objects.filter(
            date__lte=today_start, date__gte=today_start
        )

        """ set for 3 working days """
        from django.db.models import Max

        max_vote = VoteResult.objects.aggregate(max_vote=Max("total_vote"))
        max_votted_obj = VoteResult.objects.filter(
            total_vote=max_vote["max_vote"]
        ).last()
        today = datetime.now().date()
        next_day = today + timedelta(days=1)
        populate_vote = VoteResult(
            menu=max_votted_obj.menu, total_vote=max_vote["max_vote"], date=next_day
        )
        populate_vote.save()
        next_day = today + timedelta(days=2)
        populate_vote = VoteResult(
            menu=max_votted_obj.menu, total_vote=max_vote["max_vote"], date=next_day
        )
        populate_vote.save()

        vote_result_serializer = self.serializer_class(vote_results, many=True)
        return HttpUtil.success_response(
            "success", vote_result_serializer.data, status.HTTP_200_OK
        )
