from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby),
    path('register/', views.register, name='register'),
        path('Logout/',views.logout_page,name='Logout'),
    path('login/', views.Login, name='login'),
]