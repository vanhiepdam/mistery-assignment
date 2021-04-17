# -*- coding: utf-8 -*-
from rest_framework import serializers

from locations.models import City


class CitySerializerV1(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            'name',
        ]
