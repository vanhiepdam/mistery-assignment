# -*- coding: utf-8 -*-
import csv

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.db import models, transaction
from backend.models import TrackingAbstractModel, BaseModel
from locations.models import Country, City
from users.constants import USER_GENDER_CHOICES
from io import StringIO


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

    @classmethod
    def get_user_from_email(cls, email):
        return cls.objects.filter(email=email).first()

    def clear_sale_order_data(self):
        self.sale_orders.all().delete()

    def load_sale_data_from_csv_string(self, csv_string):
        f = StringIO(csv_string)
        reader = csv.reader(f, delimiter=',')
        next(reader)  # ignore first row of csv
        self.create_sale_order_from_rows(reader)

    def create_sale_order_from_rows(self, rows):
        """
        rows is a list of elements
            date, product name, sales number, revenue
            All fields are required
        """
        from sales.models.sale import SaleOrder
        from sales.models import Product
        products_map = {
            product.name: product.id
            for product in Product.objects.all()
        }
        for date, product, sales_number, revenue in rows:
            if not products_map.get(product):
                product_obj = Product.objects.create(name=product)
                products_map[product] = product_obj.id
            SaleOrder.objects.create(
                user=self,
                date=date,
                sales_number=sales_number,
                revenue=revenue,
                product_id=products_map[product]
            )
