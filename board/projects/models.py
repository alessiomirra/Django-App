from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User 
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    finish_date = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}, {self.created_by.username}"

    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk":self.pk}) 

    def update_progress(self):
        tasks = self.task_set.all()
        if tasks.count() > 0:
            completed_tasks = tasks.filter(progress = "completed")
            self.progress = int((completed_tasks.count() / tasks.count()) * 100 )
        else: 
            self.progress = 0 
        self.save()


class Task(models.Model):
    PROGRESS_CHOISES = (
        ("in progress", "in progress"), 
        ("completed", "completed"), 
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    date = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=40, blank=True, null=True)
    progress = models.CharField(max_length=40, choices=PROGRESS_CHOISES, default="in progress", blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.project.title}"

    def get_absolute_url(self):
        return reverse("task-details", kwargs={"pk":self.pk})

    def check_is_completed(self):
        return self.progress == "completed"

class Content(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_contents")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_contents")
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='files')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  


class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_comments")
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.created_by.username} for {self.project.title}"


class ProjectMembership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_projects")

    def __str__(self):
        return f"{self.user.username}, {self.project.title}"

