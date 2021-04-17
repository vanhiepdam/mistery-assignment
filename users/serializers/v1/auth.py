# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

from users.constants import DEFAULT_PASSWORD
from users.models import User


class LoginSerializerV1(serializers.Serializer):
    # write only
    email = serializers.EmailField()
    password = serializers.CharField()

    # custom
    user = None
    is_new_user = False

    def validate_email(self, value):
        user, created = User.objects.get_or_create(
            email=value,
            defaults={
                'password': DEFAULT_PASSWORD
            }
        )
        self.user = user
        self.is_new_user = created
        return value

    @staticmethod
    def _validate_info(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            raise ValidationError("Email or password is not correct")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['user'] = self.user
        password = DEFAULT_PASSWORD if self.is_new_user else attrs['password']
        self._validate_info(email=attrs['email'], password=password)
        return attrs
