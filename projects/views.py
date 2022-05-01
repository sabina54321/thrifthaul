from atexit import register
from multiprocessing import context
from re import template
from turtle import title
from authentication.views import signup
from projects.forms import ReviewForm
from .models import ProductImage, ReviewRating, product
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
     items = product.objects.filter(status=True, deletestatus=False)[0:6]
     image = product.objects.filter(status=True, deletestatus=False)[6:12]
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
    products = product.objects.filter(status=True, deletestatus=False)
    context={
        "reviews": reviews,
        "productDetails": items[0],
        "products": products
    }
    return render(request, 'productdetail.html', context)

def products(request):
    items = product.objects.filter(status=True, deletestatus=False)
    context = {'items':items}  
    return render(request, 'products.html', context) 

def editproduct(request,id):
    if request.method == "GET":
        items = product.objects.get(id=id)
        context = {'items':items}  
        return render(request, 'editproduct.html', context)
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

        items = product.objects.get(pk = id)
        items.seller = request.user
        items.phone_number = pn
        items.title = title
        items.address = add
        items.category = cat
        items.used_for = used
        items.item_price = itemprice
        items.stock = stock
        items.colour = colour
        items.material = material
        items.save()
        return redirect('profile')

def deleteproduct(request,id):
    if request.method == "POST":
        productdetail = product.objects.get(pk=id)
        productdetail.deletestatus=True
        productdetail.save()
        return redirect ('profile')

def search(request):  
    query = request.GET["query"]
    if query == "":
        return redirect(request.META["HTTP_REFERER"])
    items = product.objects.filter(Q(title__icontains=query)|Q(category__icontains=query)|Q(size__icontains=query)|Q(condition__icontains=query))
    context = {'items':items, 'query': query} 
    return render(request, 'search.html', context)

def profile(request):
    productdetail = product.objects.filter(seller__id=request.user.id, deletestatus=False)
    context = {'productdetail': productdetail}   
    return render(request, 'profile.html', context) 

def buyerviewprofile(request, id):
    items = product.objects.filter(seller__id = id, status = True, deletestatus=False)
    products = product.objects.filter(seller__id = id, status = True, deletestatus=False)
    context={
        "productDetails": items[0],
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
            data.product_id = id
            user = request.user
            data.user_id = user.id
            data.save()
            return redirect(request.META["HTTP_REFERER"])

        else:
            return redirect(request.META["HTTP_REFERER"]) 

def terms(request):
    return render(request, 'terms.html')

# def filter(request):
# 	colors=request.GET.getlist('color[]')
# 	categories=request.GET.getlist('category[]')
# 	sizes=request.GET.getlist('size[]')
# 	minPrice=request.GET['minPrice']
# 	maxPrice=request.GET['maxPrice']
# 	allProducts=product.objects.all().order_by('-id').distinct()
# 	allProducts=allProducts.filter(productattribute__price__gte=minPrice)
# 	allProducts=allProducts.filter(productattribute__price__lte=maxPrice)
# 	if len(colors)>0:
# 		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
# 	if len(categories)>0:
# 		allProducts=allProducts.filter(category__id__in=categories).distinct()
# 	if len(sizes)>0:
# 		allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
# 	t=render_to_string('products.html',{'data':allProducts})
# 	return render(request, 'filter.html',)










