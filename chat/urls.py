from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('users/', views.user_list_view, name='user_list'),
    
    path('register/', views.register, name='register'),
        path('Logout/',views.logout_page,name='Logout'),
    path('login/', views.Login, name='login'),
      # Ensure 'register' is defined
    # other URL patterns
]

   

