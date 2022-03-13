from dataclasses import dataclass
from projects.form import ProductForm
from projects.models import users
import email
import imp
from .models import product
from multiprocessing import context
from sqlite3 import Cursor
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def Register(request):
    if request.method == 'POST':
        if request.POST.get('Name') and request.POST.get('Email_Address') and request.POST.get('Password'):
            saverecord= users()
            saverecord.Name = request.POST.get('Name')
            saverecord.Email_Address = request.POST.get('Email_Address')
            saverecord.Password = request.POST.get('Password')
            saverecord.Confirm_Password = request.POST.get('Confirm_Password')
            saverecord.save()
            messages.success(request,"New User Account Has Been Registered Sucessfully...!")
            return render(request, 'Register.html')
    else:
            return render(request, 'Register.html')  

def loginUser(request):
    if request.method == "POST":
        try:
            Email = request.POST.get("Email_Address")
            Pwd = request.POST.get("Password")
            Userdetails = users.objects.get(Email_Address= Email, Password= Pwd)
            print("Name=",Userdetails)
            request.session['Email_Address']=Userdetails.Email_Address
            return render(request, 'index.html')    
        except users.DoesNotExist as e:
            messages.success(request,'Name / Password Invalid..!')
            
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
     items = product.objects.all()
     context = {'items':items}  
     return render(request, 'index.html', context)

# @login_required(login_url='login')
def Sell(request):
        if request.method == "POST":
            prod = product()
            prod.seller = request.POST.get('Name')
            prod.title = request.POST.get('Title')
            prod.category = request.POST.get('Category')
            prod.address = request.POST.get('Address')
            prod.condition = request.POST.get('Condition')
            prod.item_price = request.POST.get('Price')
            prod.price_negotiable = request.POST.get('Negotiable')
            prod.description = request.POST.get('Description')
            prod.product_image = request.POST.get('image') 

            if len(request.FILES) != 0:
                prod.product_image = request.FILES['image']

            prod.save()
            messages.success(request, "Product added sucessfully")
            return redirect('/')
        return render(request, 'Sell.html')

def productdetail(request):
    return render(request, 'productdetail.html') 




  



