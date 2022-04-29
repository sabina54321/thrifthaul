from base64 import urlsafe_b64decode
from lib2to3.pgen2 import token
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
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.conf import settings 
from django.contrib.auth.tokens import PasswordResetTokenGenerator

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
        messages.add_message(request, messages.ERROR,
                                'Wrong Credentials')
        return render(request, 'authentication/register.html')    
        

def loginuser(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR,
                                'Wrong Credentials')
            return render(request, 'authentication/login.html') 

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

def editprofile(request):
    if request.method == "POST":
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        un = request.POST["uname"]
        con = request.POST["contact"]
        add = request.POST["address"]
        pp = request.FILES["image"]

        user = User.objects.get(id=request.user.id)
        user.first_name = fn
        user.last_name = ln
        user.username = un
        user.phone_number = con
        user.address = add
        user.profileimage = pp
        user.save()
        return redirect('profile')
    return render(request, 'editprofile.html')



def RequestResetPassword(request):
    if request.method == "GET":
        return render(request, 'authentication/requestresetpassword.html')

    if request.method == "POST":
        email = request.POST['email']

        # if not validate_email(email):
        #     messages.error(request,'Please enter a valid email')
        #     return render(request, 'authentication/requestresetpassword.html')

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = 'Reset your Password'
            email_body = render_to_string('authentication/resetuserpassword.html',
            {
                'domain': current_site.domain,
                'userid': urlsafe_base64_encode(force_bytes((user[0].pk))),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            })
            emailmessage=EmailMessage(subject=email_subject,body=email_body, 
                               from_email = settings.EMAIL_FORM_USER,
                               to=[email]) 


            emailmessage.send()

            messages.success(request,'We have sent you an email with instruction on how to reset password')
            return render(request, 'authentication/requestresetpassword.html')
        else:
            messages.success(request,'Invalid Username.')
            return render(request, 'authentication/requestresetpassword.html')

def SetNewPassword(request, useridb64, token):
    if request.method == "GET":
        context = {'useridb64': useridb64, 'token': token}
        return render(request, 'authentication/setnewpassword.html', context)

    if request.method == "POST":
        context = {'useridb64': useridb64, 'token': token}
        password = request.POST.get('password')
        
    try:
        userid = force_str(urlsafe_base64_decode(useridb64))

        user = User.objects.get(pk=userid)
        user.set_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Password changed, now you can login')
        return redirect('login')
    except Exception as e:
        messages.add_message(request, messages.SUCCESS, 'Something went wrong')
        return render(request, 'authentication/setnewpassword.html', context)
