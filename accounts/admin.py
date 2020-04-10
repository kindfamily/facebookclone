from django.contrib import admin
from .models import Profile
from accounts.models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'nickname', 'user']
    list_display_links = ['nickname', 'user']
    search_fields = ['nickname']
    
@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['current_user', 'user', 'created_at']
    list_display_links = ['current_user', 'user']
    
@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user', 'created_at']
    list_display_links = ['from_user', 'to_user', 'created_at']