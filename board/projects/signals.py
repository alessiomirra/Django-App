from django.db.models.signals import post_save 
from django.dispatch import receiver 

from .models import Task 

#### 

@receiver(post_save, sender=Task)
def update_project_progress(sender, instance, **kwags):
    instance.project.update_progress() 

