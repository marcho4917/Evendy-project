from django.urls import path
from . import views as notices_views

urlpatterns = [
    path('notices-list/', notices_views.NoticesListView.as_view(), name='notices_list'),
    path('', notices_views.send_invite, name='send_invite')
]