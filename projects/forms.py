from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import ReviewRating, product

class ProductForm(forms.Form):
    name= forms.CharField(max_length=200)
    price = forms.FloatField()

class ReviewForm(ModelForm):
    subject = forms.CharField(max_length=100, required=False)
    review = forms.CharField(widget = forms.Textarea, max_length=100, required=False)
    rating = forms.IntegerField(required=False)
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']    
    