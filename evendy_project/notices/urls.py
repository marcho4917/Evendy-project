from django.urls import path
from . import views as notices_views

urlpatterns = [
    path('notices-list/', notices_views.NoticesListView.as_view(), name='notices_list'),
    path('<int:event_id>/<int:profile_id>/', notices_views.send_invite, name='send_invite'),
path('invites-list/', notices_views.InvitesListView.as_view(), name='invites_list'),
]