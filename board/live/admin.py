from django.contrib import admin
from .models import ChatMessage, Notification 
# Register your models here.

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_filter = ["project", "user"]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter = ["project"]