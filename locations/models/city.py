# -*- coding: utf-8 -*-
from django.db import models

from backend.models import TrackingAbstractModel
from locations.models.country import Country


class City(TrackingAbstractModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=500)
