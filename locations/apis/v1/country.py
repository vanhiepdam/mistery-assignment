# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins

from locations.models import Country
from locations.serializers.v1.country import CountrySerializerV1


class CountryViewsetV1(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CountrySerializerV1
    queryset = Country.objects.all().prefetch_related('cities')
    pagination_class = None
