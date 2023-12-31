from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers, status

from .models import Employee


class EmployeeSerializer(serializers.Serializer):
    guid = serializers.CharField(read_only=True, source="guid.hex")
    email = serializers.EmailField(allow_blank=False)
    first_name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    date_joined = serializers.DateTimeField(required=False)
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = Employee.objects.filter(email=attrs.get("email")).exists()
        if email:
            raise ValidationError(
                "Employee with email exists", code=status.HTTP_403_FORBIDDEN
            )

        if attrs.get("password") != attrs.get("confirm_password"):
            raise ValidationError(
                "Password doesn't match!", code=status.HTTP_400_BAD_REQUEST
            )

        return super().validate(attrs)

    def create(self, validated_data):
        if validated_data.get("password") != validated_data.pop("confirm_password"):
            raise ValidationError(
                "Confirm password doesn't match", code=status.HTTP_403_FORBIDDEN
            )

        else:
            new_user = Employee(**validated_data)
            new_user.password = make_password(validated_data.get("password"))
            new_user.save()
            return new_user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance
