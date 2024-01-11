from django.urls import path
from . import views as evendy_views
from django.contrib.auth import views


urlpatterns = [
    path('', evendy_views.EventListView.as_view(), name='events_list'),
    path('register/', evendy_views.register, name='register'),
    path('login/', views.LoginView.as_view(template_name='evendy/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='evendy/logout.html'), name='logout'),
    path('profile/', evendy_views.profile, name='profile'),
    path('event-details/', evendy_views.event_details, name='event_details'),
    path('events-list/', evendy_views.EventListView.as_view(), name="events_list"),
]


