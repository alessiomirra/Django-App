from django.contrib import admin
from .models import ChatMessage 
# Register your models here.

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_filter = ["project", "user"]