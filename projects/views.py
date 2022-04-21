from atexit import register
from multiprocessing import context
from re import template
from turtle import title
from authentication.views import signup
from projects.forms import ReviewForm
from .models import ProductImage, ReviewRating, product
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
     items = product.objects.all()[0:6]
     image = product.objects.all()[6:12]
     context = {'items':items, 'image': image}  
     return render(request, 'index.html', context)

@login_required 
def Sell(request):
        if request.method == "POST":
            prod = product()
            prod.seller_name = request.POST.get('Name')
            prod.seller = request.user
            prod.phone_number = request.POST.get('Number')
            prod.title = request.POST.get('Title')
            prod.category = request.POST.get('Category')
            prod.address = request.POST.get('Address')
            prod.email_address = request.POST.get('Email')
            prod.used_for = request.POST.get('Usedfor')
            prod.size = request.POST.get('Size')
            prod.condition = request.POST.get('Condition')
            prod.item_price = request.POST.get('Price')
            prod.price_negotiable = request.POST.get('Negotiable')
            prod.colour = request.POST.get('Colour')
            prod.material = request.POST.get('Material')
            prod.description = request.POST.get('Description') 
            prod.product_image = request.POST.get('image') 
            prod.stock = request.POST.get('Stock') 

            if len(request.FILES) != 0:
                prod.product_image = request.FILES['image']

            prod.save()

            images = request.FILES.getlist('productimage')
            for img in images:
                ProductImage.objects.create(product=prod,image=img)
            messages.success(request, "Product added sucessfully")
            return redirect('/')
        return render(request, 'Sell.html')

def productdetail(request, id):
    items = product.objects.filter(id = id)
    reviews = ReviewRating.objects.filter(product_id = id)
    products = product.objects.all()
    context={
        "productDetails": items[0],
         "reviews": reviews,
         "products": products
    }
    return render(request, 'productdetail.html', context)

def products(request):
     items = product.objects.all()
     context = {'items':items}  
     return render(request, 'products.html', context) 

def editproduct(request):
    if request.method == "POST":
        pn = request.POST["pnum"]
        title = request.POST["title"]
        add = request.POST["address"]
        cat = request.POST["category"]
        used = request.POST["usedfor"]
        itemprice = request.POST["price"]
        stock = request.POST["stock"]
        colour = request.POST["colour"]
        material = request.POST["material"]

        product = product.objects.get(id=request.product.id)
        product.phone_number = pn
        product.title = title
        product.address = add
        product.category = cat
        product.used_for = used
        product.item_price = itemprice
        product.stock = stock
        product.colour = colour
        product.material = material
        product.save()
        return redirect('profile')
    return render(request, 'editproduct.html')

def deleteproduct(request,id):
    if request.method == "POST":
        productdetail = product.objects.get(id =id)
        productdetail.delete()
        return redirect ('profile')

def search(request):  
    query = request.GET["query"]
    items = product.objects.filter(Q(title__icontains=query)|Q(category__icontains=query))
    context = {'items':items, 'query': query} 
    return render(request, 'search.html', context)

def profile(request):
    productdetail = product.objects.filter(seller__id=request.user.id)
    context = {'productdetail': productdetail}   
    return render(request, 'profile.html', context)

def buyerviewprofile(request, id):
    items = product.objects.filter(seller__id = id)
    reviews = ReviewRating.objects.filter(product_id = id)
    products = product.objects.filter(seller__id = id)
    context={
        "productDetails": items[0],
         "reviews": reviews,
         "products": products
    }
    return render(request, 'buyerviewprofile.html', context)

def submitreview(request, id):
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            data = ReviewRating()
            data.review = form.cleaned_data["review"]
            data.rating = form.cleaned_data["rating"]
            data.seller_id = id
            user = request.user
            data.user_id = user.id
            data.save()
            return redirect(request.META["HTTP_REFERER"])










