from datetime import datetime
from distutils.command.upload import upload
from email.policy import default
from hashlib import blake2b
import imp
from pyexpat import model
from re import T
from tkinter import CASCADE
from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import User
import os

from django.forms import BooleanField
from authentication.models import User

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = "%s%s", (timeNow,old_filename)
    return os.path.join('upload/', filename)

CATEGORY_CHOICES = (

    ('w', 'Womens Wear'),
    ('M', 'Mens Wear'),
    ('K', 'Kids Wear'),
    ('P', 'Party Bag'),
    ('H', 'Hand Bag'),
    ('S', 'Side Bag'),
    
)

CONDITION_CHOICES = (
    ('G', 'Good'),
    ('O', 'old'),
    ('N', 'New'),
)

SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)

NEGOTIABLE_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),                                                                                                                
)
class product(models.Model):
    seller_name = models.CharField(max_length=100, null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)
    used_for = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=100, null=True, blank=True)
    item_price = models.FloatField()
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=10, null=True, blank=True)
    price_negotiable = models.CharField(choices=NEGOTIABLE_CHOICES, max_length=5, null=True, blank=True)
    colour = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    product_image = models.ImageField(upload_to="productimg", null=True, blank=True)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    def __str__(self):
        return str(self.title) 

class ProductImage(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "productimg")

    def __str__(self):
        return self.product.title 

class ReviewRating(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(blank=True, default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title






        

