from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*

from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout 
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
@login_required(login_url="/login/")
def lobby(request,sender=User):
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
            next_url = request.GET.get('next', '/')  # Redirect to 'next' or default to '/chat/'
            return redirect(next_url)
        
    return render(request, 'login.html')
def logout_page(request):
    logout(request)
    return redirect('/login/')

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



# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


from django.utils import timezone
from pytz import timezone as tz
from .models import Profile

def user_activity_view(request):
    profiles = Profile.objects.all()
    indian_timezone = tz('Asia/Kolkata')  # Get IST time zone

    for profile in profiles:
        # Convert last_active to IST (if it's not None)
        if profile.last_active:
            profile.last_active = timezone.localtime(profile.last_active, indian_timezone)
    
    return render(request, 'user_activity.html', {'profiles': profiles})

from django.views.decorators.csrf import csrf_exempt
from .models import Profile
from django.http import JsonResponse
@csrf_exempt  # Use csrf_exempt for simplicity in testing, or use csrf tokens in production
@login_required
def update_typing_status(request):
    if request.method == "POST":
        # Get the current user
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Update last active time to now (could also set `online` status here if you prefer)
        profile.last_active = timezone.now()
        profile.save()
        
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"})

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




def user_view(request):
    users = User.objects.all() 
    print(users)
    return render(request, 'your_template.html', {'users': users})
