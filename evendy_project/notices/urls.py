from django.urls import path, include
from . import views as notices_views

urlpatterns = [
    path('', include('evendy.urls')),
    path('notices-list/', notices_views.NoticesListView.as_view(), name='notices_list'),
    path('<int:event_id>/<int:profile_id>/', notices_views.send_invite, name='send_invite'),
    path('invites-list/', notices_views.InvitesListView.as_view(), name='invites_list'),
    path('<int:invite_id>/<int:profile_id>/<int:event_id>', notices_views.accept_or_decline_invitation, name='accept_or_decline_invitation')
]