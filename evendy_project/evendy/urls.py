from django.urls import path, include
from . import views as evendy_views
from django.contrib.auth import views

urlpatterns = [
    #path('', evendy_views.EventListView.as_view(), name='events_list'),
    path('register/', evendy_views.register, name='register'),
    path('login/', views.LoginView.as_view(template_name='evendy/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='evendy/logout.html'), name='logout'),
    path('profile/', evendy_views.profile, name='profile'),
    path('event-details/<int:event_id>/', evendy_views.event_details, name='event_details'),
    #path('events-list/', evendy_views.EventListView.as_view(), name="events_list"),
    path('event-details/<int:event_id>/add-or-delete', evendy_views.add_or_remove_user_from_seekers, name='add_or_remove_user_from_seekers'),
    path('search-events/', evendy_views.search_events, name='search_events'),
    path('profile-details/<int:user_id>', evendy_views.profile_details, name='profile_details'),
    path('my-events/', evendy_views.show_my_events, name='show_my_events')
]


