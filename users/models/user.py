# -*- coding: utf-8 -*-
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models
from backend.models import TrackingAbstractModel, BaseModel
from locations.models import Country, City
from users.constants import USER_GENDER_CHOICES


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    gender = models.CharField(choices=USER_GENDER_CHOICES, null=True, blank=True, max_length=30)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.ForeignKey(
        Country,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )
    city = models.ForeignKey(
        City,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='users'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, null=True, help_text='Updated at')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser and self.is_staff

    def save(self, *args, **kwargs):
        if not self.check_password(self.password):
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    @classmethod
    def get_user_from_email(cls, email):
        return cls.objects.filter(email=email).first()
