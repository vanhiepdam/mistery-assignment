# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import reverse

from sales.forms.sale_order import UpdateSaleOrderForUserForm
from sales.models import SaleOrder
from users.models import User


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'sales_number', 'revenue']

    def get_urls(self):
        urls = super(SaleOrderAdmin, self).get_urls()
        admin_site = self.admin_site
        additional_urls = [
            url(r"^update-sale-order-for-user/$", admin_site.admin_view(self.update_sale_order_for_user),
                name='update-sale-order-for-user'),
        ]
        return additional_urls + urls

    def update_sale_order_for_user(self, request):
        model = self.model
        opts = model._meta
        users = User.objects.filter(is_staff=False)
        form = UpdateSaleOrderForUserForm()
        context = dict(
            self.admin_site.each_context(request),
            opts=opts,
            app_label=opts.app_label,
            users=users,
            form=form
        )
        if request.method == 'POST':
            form = UpdateSaleOrderForUserForm(request.POST)
            if form.is_valid():
                form.update_sale_order_for_user()
                self.message_user(request, 'Import success', messages.SUCCESS)
                return redirect(reverse('admin:sales_saleorder_changelist'))
            else:
                self.message_user(request, 'Failed', messages.ERROR)
        return render(
            request,
            template_name='admin/sales/saleorder/update_sale_order_for_user.html',
            context=context
        )
