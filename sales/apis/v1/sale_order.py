# -*- coding: utf-8 -*-
from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from sales.models import SaleOrder
from sales.serializers.v1.sale_order import ListSaleOrderSerializerV1, CreateUpdateSaleOrderSerializerV1
from sales.services.v1.product import ProductService


class SaleOrderViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin
):
    pagination_class = None

    def get_queryset(self):
        return SaleOrder.objects.filter(user=self.request.user).select_related(
            'product',
            'user'
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return ListSaleOrderSerializerV1
        return CreateUpdateSaleOrderSerializerV1

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['product_name_map'] = ProductService.get_product_name_map()
        return context

    def create(self, request, *args, **kwargs):
        data = request.data.get('sales_data')
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            request.user.clear_sale_order_data()
            serializer.save()
        return Response(status.HTTP_201_CREATED)
