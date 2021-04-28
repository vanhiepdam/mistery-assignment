# -*- coding: utf-8 -*-
from django.contrib import admin

from locations.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fields = search_fields = ['name']
