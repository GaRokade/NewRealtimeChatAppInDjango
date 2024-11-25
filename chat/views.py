from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*

from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout 
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def lobby(request):
    return render(request, 'lobby.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=User.objects.filter(username=username)
        if user.exists():
           messages.info(request,"username is Already Taken")
           return redirect('/register')
        user=User.objects.create(
            first_name=first_name,
        
            last_name=last_name,
            username=username,
            
        )
        
        user.set_password(password)
        user.save()
        messages.info(request,"The account Created Successfully")
        return redirect('/register/')
    return render(request,'register.html')   

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.info(request, "Invalid Password")
            return redirect('/login/')
        else:
            auth_login(request, user)
            next_url = request.GET.get('next', '/chat/')  # Redirect to 'next' or default to '/chat/'
            return redirect(next_url)
        
    return render(request, 'login.html')
def logout_page(request):
    logout(request)
    return redirect('/login/')

