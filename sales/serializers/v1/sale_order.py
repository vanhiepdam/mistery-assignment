# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from sales.models import SaleOrder, Product


class ListSaleOrderSerializerV1(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')
    revenue = serializers.FloatField()
    sales_number = serializers.IntegerField()
    date = serializers.DateField()
    user_id = serializers.IntegerField()

    class Meta:
        model = SaleOrder
        fields = (
            'id',
            'product',
            'revenue',
            'sales_number',
            'date',
            'user_id'
        )


class CreateUpdateSaleOrderSerializerV1(serializers.ModelSerializer):
    product = serializers.CharField()
    revenue = serializers.FloatField()
    sales_number = serializers.IntegerField()
    date = serializers.DateField()
    user_id = serializers.IntegerField()

    class Meta:
        model = SaleOrder
        fields = (
            'product',
            'revenue',
            'sales_number',
            'date',
            'user_id',
        )

    def validate_user_id(self, value):
        return self.context['request'].user.id

    def validate_product(self, value):
        return self.context['product_name_map'].get(value)
