# -*- coding: utf-8 -*-
from django import forms

from users.models import User


class UpdateSaleOrderForUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False))
    sale_data = forms.CharField(widget=forms.Textarea())

    def update_sale_order_for_user(self):
        user = self.cleaned_data['user']
        user.load_sale_data_from_csv_string(csv_string=self.cleaned_data['sale_data'])
