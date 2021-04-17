# -*- coding: utf-8 -*-
from rest_framework import serializers
from locations.serializers.v1.city import CitySerializerV1
from locations.models import Country


class CountrySerializerV1(serializers.ModelSerializer):
    cities = CitySerializerV1(many=True)

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'cities',
        )
