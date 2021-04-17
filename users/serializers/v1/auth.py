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
        )
        self.user = user
        self.is_new_user = created
        return value

    @staticmethod
    def _validate_info(user, password):
        if user.check_password(password):
            raise ValidationError(detail="Email or password is not correct")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['user'] = self.user
        if self.is_new_user:
            self.user.set_password(attrs['password'])
            self.user.save()
        self._validate_info(user=self.user, password=attrs['password'])
        return attrs
