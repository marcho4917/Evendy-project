from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='evendy-home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='evendy/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='evendy/logout.html')),
    path('profile/', views.profile, name='profile'),
]