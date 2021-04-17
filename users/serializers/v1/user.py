# -*- coding: utf-8 -*-
from rest_framework import serializers

from locations.models import Country, City
from users.models import User


class UserSerializerV1(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'age',
            'country',
            'city'
        )
