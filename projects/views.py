from multiprocessing import context
from re import template
from .models import ProductImage, product
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# def Register(request):
#     if request.method == 'POST':
#         if request.POST.get('Name') and request.POST.get('Email_Address') and request.POST.get('Password'):
#             saverecord= users()
#             saverecord.Name = request.POST.get('Name')
#             saverecord.Email_Address = request.POST.get('Email_Address')
#             saverecord.Password = request.POST.get('Password')
#             saverecord.Confirm_Password = request.POST.get('Confirm_Password')
#             saverecord.save()
#             messages.success(request,"New User Account Has Been Registered Sucessfully...!")
#             return render(request, 'Register.html')
#     else:
#             return render(request, 'Register.html')  

# def loginUser(request):
#     if request.method == "POST":
#         try:
#             Email = request.POST.get("Email_Address")
#             Pwd = request.POST.get("Password")
#             Userdetails = users.objects.get(Email_Address= Email, Password= Pwd)
#             print("Name=",Userdetails)
#             request.session['Email_Address']=Userdetails.Email_Address
#             return redirect('index')    
#         except users.DoesNotExist as e:
#             messages.success(request,'Name / Password Invalid..!')
            
#     return render(request, 'login.html')

# def logoutUser(request):
#     try:
#         del request.session['Email_Address']
#         return redirect('index') 
#     except:
#         return redirect('index') 


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
    context={
        "productDetails": items[0]
    }
    return render(request, 'productdetail.html', context)

def products(request):
     items = product.objects.all()
     context = {'items':items}  
     return render(request, 'products.html', context)

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





