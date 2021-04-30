from io import StringIO

from django import forms
import csv

from django.db import transaction

from locations.models import Country, City
from sales.models import SaleOrder, Product
from users.constants import USER_GENDER_CHOICES, USER_GENDER_MALE
from users.models import User


class UserAdminForm(forms.Form):
    initial_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    is_superuser = forms.BooleanField(required=False, initial=False, help_text='Make user as admin with all permissions')
    is_staff = forms.BooleanField(required=False, initial=False, help_text='Make user as admin with specific permissions')
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput())
    gender = forms.ChoiceField(choices=USER_GENDER_CHOICES)
    age = forms.IntegerField()
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    city = forms.ModelChoiceField(queryset=City.objects.all())
    input_sale_data = forms.CharField(required=False, widget=forms.Textarea())

    class Meta:
        fields = (
            'initial_id',
            'is_superuser',
            'is_staff',
            'email',
            'password',
            'password_confirmation',
            'gender',
            'age',
            'country',
            'city',
            'input_sale_data',
        )

    def clean_email(self):
        is_new_instance = not bool(self.cleaned_data['initial_id'])
        queryset = User.objects.filter(email=self.cleaned_data['email'])
        if not is_new_instance:
            queryset = queryset.exclude(id=self.cleaned_data['initial_id'])
        if queryset.exists():
            raise forms.ValidationError("Email existed")
        return self.cleaned_data['email']

    def clean_password_confirmation(self):
        if self.cleaned_data['password'].startswith('pbkdf2_sha256$'):
            return self.cleaned_data['password_confirmation']
        if self.cleaned_data['password_confirmation'] != self.cleaned_data['password']:
            raise forms.ValidationError("2 passwords are not match")
        return self.cleaned_data['password_confirmation']

    def clean_city(self):
        if self.cleaned_data['city'].country != self.cleaned_data['country']:
            raise forms.ValidationError("City not in selected country")
        return self.cleaned_data['city']

    def _create_user(self):
        user = User(
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            age=self.cleaned_data['age'],
            country=self.cleaned_data['country'],
            city=self.cleaned_data['city'],
            is_superuser=self.cleaned_data.get('is_superuser', False),
            is_staff=self.cleaned_data.get('is_staff', False),
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        self._update_sale_data(user)
        return user

    def _update_user(self):
        user = User.objects.get(id=self.cleaned_data['initial_id'])
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.age = self.cleaned_data['age']
        user.country = self.cleaned_data['country']
        user.city = self.cleaned_data['city']
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        user.is_staff = self.cleaned_data.get('is_staff', False)
        if user.password != self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        user.save()
        self._update_sale_data(user)
        return user

    def _update_sale_data(self, user):
        if not self.cleaned_data.get('input_sale_data'):
            return
        user.load_sale_data_from_csv_string(csv_string=self.cleaned_data.get('input_sale_data'))

    def create_update_user(self):
        is_new_instance = not bool(self.cleaned_data['initial_id'])
        with transaction.atomic():
            if is_new_instance:
                return self._create_user()
            return self._update_user()
