# -*- coding: utf-8 -*-
from rest_framework import routers
from django.urls import path, include

from locations.apis.v1.country import CountryViewsetV1
from sales.apis.v1.sale_order import SaleOrderViewset
from users.apis.v1.auth import LoginViewsetV1
from users.apis.v1.user import UserViewsetV1

router = routers.DefaultRouter(trailing_slash=False)
router.register('', LoginViewsetV1, basename='auth')
router.register('users', UserViewsetV1, basename='users')
router.register('country_data', CountryViewsetV1, basename='country_data')
router.register('sales', SaleOrderViewset, basename='sales')


urlpatterns = [
    path('', include(router.urls)),
]
