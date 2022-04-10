from django.contrib import admin

# Register your models here.
from .models import ProductImage, ReviewRating, product
# from .models import profile

admin.site.register(product)
# class ProductModel(admin.ModelAdmin):
#     list_display=['title','category','address','item_price',' condition','product_image','description']

# admin.site.register(profile)
admin.site.register(ProductImage)


admin.site.register(ReviewRating)