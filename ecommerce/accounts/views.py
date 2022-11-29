from django.shortcuts import render, redirect
from django.contrib.auth.models import User #from django.contrib.auth app (package) of django, models module,
                                            #import the User model
from core.models import * #from the core app, models module, import all models and functions.                  
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .helpers import send_forget_password_mail

def user_login(request):
    if request.method == "POST":   #if the user is tring to submit the form or filling in the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.info(request, "Wrong Username or Password.")
    return render(request, 'accounts/login.html') #render the login.html file in accounts folder

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')
        #print(username, email)
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Exists.")
                return redirect('user_register')
            else:
                if User.objects.filter(email=email).exists():
                    
                    messages.info(request, "Email Already Exists.")
                    return redirect('user_register')
                else: 
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    data = Customer(user = user, phone_field=phone)
                    data.save()
        
                    
                    #code for login of user
                    our_user = authenticate(username=username, password=password)
                    if our_user is not None:
                        login(request, user)
                        return redirect('/')
        else:
            messages.info(request, "Mismatch of password and confirm password.")
            return redirect('user_register')
    return render(request, 'accounts/register.html') 

def user_logout(request):
    logout(request)
    return redirect('/')

def not_registered(request):
    return redirect('user_register')

def already_member(request):
    return redirect('user_login')

def changepassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        print(profile_obj)
        
        
        
    except Exception as e:
        print(e)
    
    
    
    return render(request, 'accounts/change_password.html')

import uuid

def forgetpassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, "There is no user with this username")
                return redirect('forget_password')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj, token)
            messages.success(request, "An email is sent")
            return redirect('forget_password')
            
            
            
    except Exception as e:
        print(e)
    return render(request, 'accounts/forget-password.html')
        