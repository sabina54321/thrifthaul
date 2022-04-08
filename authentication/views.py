from base64 import urlsafe_b64decode
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from email import message
from multiprocessing import context
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.urls import reverse
from authentication.forms import CreateUserForm 
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from authentication.models import User
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

def send_action_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('authentication/activate.html',{
        'user':user,
        'domain':current_site,
        'userid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })

    email=EmailMessage(subject=email_subject,body=email_body, 
                       from_email = settings.EMAIL_FORM_USER,
                       to=[user.email]) 

    email.send()

def signup(request):
    if request.method=="POST":  
        user=CreateUserForm(request.POST)
    
        if user.is_valid():
            form = user.save()


            send_action_email(form,request)

            messages.success(request, 'Please check your email for verification' )
            return redirect('login')
        else :
            if user.errors:
                return render(request, "authentication/register.html", {"errors": user.errors})
    else: 
        return render(request, 'authentication/register.html')    
        

def loginuser(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)

        if not user.is_email_verified:
            messages.add_message(request, messages.ERROR,
                                'Email is not verified, please check your email inbox')
            return render(request, 'authentication/login.html', context)

        if user is not None:
            login(request, user)
            return redirect('index')

    return render(request,"authentication/login.html")


def logoutuser(request):
    logout(request)
    return redirect("index")


def activate_user(request, useridb64, token):

    try:
        userid = force_str(urlsafe_base64_decode(useridb64))

        user = User.objects.get(pk=userid)
    
    except Exception as e:
        user=None

    if user and generate_token.check_token(user,token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified, now you can login')
        return redirect(reverse('login'))


    return render(request,'authentication/activate-failed.html', {"user":user})