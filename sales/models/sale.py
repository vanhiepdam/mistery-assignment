# -*- coding: utf-8 -*-
from django.db import models

from backend.models import TrackingAbstractModel
from sales.models.product import Product
from users.models import User


class SaleOrder(TrackingAbstractModel):
    product = models.ForeignKey(
        Product,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='sale_orders'
    )
    date = models.DateField()
    sales_number = models.IntegerField()
    revenue = models.FloatField()
    user = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='sale_orders'
    )
