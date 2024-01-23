from django.shortcuts import render, redirect
from .models import Room, Message


def chat_page(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chat_page.html", context)
