from django.urls import path, include
from chat import views as chat_views

urlpatterns = [
    path("", chat_views.chat_page, name="chat_page")
]