# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins

from users.models import User
from users.serializers.v1.user import UserSerializerV1


class UserViewsetV1(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
):
    serializer_class = UserSerializerV1
    queryset = User.objects.all().select_related('country', 'city')
