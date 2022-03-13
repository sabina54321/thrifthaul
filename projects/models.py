from datetime import datetime
import email
from django.db import models
from django.forms import PasswordInput
import os

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = "%s%s", (timeNow,old_filename)
    return os.path.join('upload/', filename)

class users(models.Model):
    Name=models.CharField(max_length=100)
    Email_Address=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    Confirm_Password=models.CharField(max_length=100)
    class Meta:
        db_table="users"

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

NEGOTIABLE_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
)
class product(models.Model):
    seller = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    item_price = models.FloatField()
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=10, null=True, blank=True)
    price_negotiable = models.CharField(choices=NEGOTIABLE_CHOICES, max_length=5, null=True, blank=True)
    # product_image = models.ImageField(upload_to=filepath, null=True, blank=True)
    product_image = models.ImageField(upload_to="productimg")
    description = models.TextField()
    def __str__(self):
        return str(self.title)

