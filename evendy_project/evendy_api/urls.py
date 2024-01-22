from django.urls import path
from .views import events_list

urlpatterns = [
    path('events/', events_list, name='events_list'),
    #path('events/', oli, name='oli'),
]