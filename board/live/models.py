from django.db import models 
from django.contrib.auth.models import User 
from projects.models import Project 
# Create your models here.

class ChatMessage(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_messages")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_messages")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} message for {self.project.title} 's chat room"

