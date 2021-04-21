# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.response import Response

from sales.services.v1.sale_order import SaleOrderService


class SaleStatisticViewset(viewsets.GenericViewSet):
    def list(self, request):
        user = request.user
        data = SaleOrderService().get_statistic_by_user(user)
        return Response(data)
