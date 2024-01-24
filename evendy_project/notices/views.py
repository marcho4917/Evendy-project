from django.views.generic.list import ListView
from .models import Notice


class NoticesListView(ListView):
    model = Notice
    template_name = 'notice/notices_list.html'


def send_invite(request):
    if request.method == 'POST':
        pass

