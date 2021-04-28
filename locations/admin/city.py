# -*- coding: utf-8 -*-
from django.contrib import admin

from locations.models import City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    fields = search_fields = ['name']
