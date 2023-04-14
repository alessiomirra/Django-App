from django.contrib import admin
from .models import Project, Task, Content, Comment, ProjectMembership 
# Register your models here.

class TaskInline(admin.StackedInline):
    model = Task 

class ContentInline(admin.StackedInline):
    model = Content 

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "created_by", "date", "progress"]
    inlines = [ TaskInline, ContentInline ]

admin.site.register(Comment)
admin.site.register(ProjectMembership)