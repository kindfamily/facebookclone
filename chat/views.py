from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from accounts.models import *
import logging

# Create your views here.
def chat_list(request):
    user = request.user
    user_profile = user.profile
    
    friends = user.friends.all()
    
    return render(request, 'chat/chat_list.html', {
        'user_profile': user_profile,
        'friends': friends,
    })

def room(request, room_id):
    user = request.user
    user_profile = user.profile

    friends = user.friends.all()

    room = Room.objects.get(pk=room_id)
    friend_user = room.users.all().exclude(pk=user.id).first()

    return render(request, 'chat/room.html', {
        'current_user': user,
        'user_profile': user_profile,
        'friends': friends,
        'room': room,
        'friend_user': friend_user,
    })



















    