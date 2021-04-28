# -*- coding: utf-8 -*-
from django.db import models

from backend.models import TrackingAbstractModel


class Product(TrackingAbstractModel):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
