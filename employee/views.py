from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions
from core.http_util import HttpUtil
from validate_email import validate_email
from .serializers import EmployeeSerializer
import logging

logger = logging.getLogger(__name__)


class RegisterAPIView(GenericAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        payload = request.data
        if not payload["email"]:
            return HttpUtil.error_response("Email is required")
        is_valid_email = validate_email(payload["email"])
        if not is_valid_email:
            return HttpUtil.error_response("Invalid email address")
        employee_serializer = EmployeeSerializer(data=payload)
        if employee_serializer.is_valid():
            employee_serializer.save()
            return HttpUtil.success_response(
                "user created successfully.",
                {},
                status.HTTP_201_CREATED,
            )
        else:
            logger.error(
                employee_serializer.errors,
                extra={
                    "user_email": payload["email"],
                },
            )
            return HttpUtil.error_response(employee_serializer.errors)
