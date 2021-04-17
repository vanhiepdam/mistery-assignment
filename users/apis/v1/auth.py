# -*- coding: utf-8 -*-
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.serializers.v1.auth import LoginSerializerV1
from users.services.v1.auth import AuthServiceV1


class LoginViewsetV1(viewsets.GenericViewSet):
    @action(
        detail=False,
        methods=['POST'],
        url_path='login',
        serializer_class=LoginSerializerV1,
        permission_classes=[AllowAny]
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AuthServiceV1.get_token_for_user(user)
        return Response({
            'token': token.key,
            'user_id': user.id,
        })

    @action(
        detail=False,
        methods=['GET'],
        url_path='logout',
        permission_classes=[IsAuthenticated]
    )
    def logout(self, request):
        user = request.user
        AuthServiceV1.logout_user(user)
        return Response(status.HTTP_200_OK)
