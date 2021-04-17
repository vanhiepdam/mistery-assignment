# -*- coding: utf-8 -*-
from rest_framework.authtoken.models import Token


class AuthServiceV1:
    @classmethod
    def get_token_for_user(cls, user):
        token, _ = Token.objects.get_or_create(
            user=user
        )
        return token

    @classmethod
    def logout_user(cls, user):
        Token.objects.filter(user=user).delete()
