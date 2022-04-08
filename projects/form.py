from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import product

class ProductForm(forms.Form):
    name= forms.CharField(max_length=200)
    price = forms.FloatField()
    