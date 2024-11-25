from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import Profile
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

@receiver(user_logged_in)
def update_last_active(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)  # Get or create profile for the user
    profile.last_active = timezone.now()  # Update last active time to now
    profile.save()

@login_required
def user_list_view(request):
    profiles = Profile.objects.all()  # Get all profiles
    return render(request, 'user_list.html', {'profiles': profiles})
 
 # signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
