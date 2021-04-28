# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import reverse

from users.forms.user import UserAdminForm
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    autocomplete_fields = [
        'country',
        'city'
    ]

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        instance = self.get_object(request, object_id)
        form = UserAdminForm()
        if object_id:
            form.initial = {
                'initial_id': instance.id,
                'email': instance.email,
                'password': instance.password,
                'gender': instance.gender,
                'age': instance.age,
                'country': instance.country,
                'city': instance.city
            }
        extra_context['form'] = form
        return super().changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        admin_site = self.admin_site
        additional_urls = [
            url(r"^create-update/$", admin_site.admin_view(self.create_update_user), name='create_update_user'),
            url(r"^clear-sale-information/$", admin_site.admin_view(self.clear_sale_information), name='clear_sale_information'),
        ]
        return additional_urls + urls

    def create_update_user(self, request, extra_context=None):
        form = UserAdminForm(data=request.POST)
        if form.is_valid():
            form.create_update_user()
            self.message_user(request, f"Save successfully", messages.SUCCESS)
            return redirect(reverse('admin:users_user_changelist'))
        self.message_user(request, form.errors, messages.ERROR)
        return redirect(reverse('admin:users_user_changelist'))

    def clear_sale_information(self, request):
        User.objects.get(id=request.POST['user_id']).clear_sale_order_data()
        self.message_user(request, f"Clear successfully", messages.SUCCESS)
        return redirect(reverse('admin:users_user_changelist'))
