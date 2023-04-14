from django.shortcuts import render, get_object_or_404 
from django.contrib.auth.decorators import login_required
from projects.models import Project 

# Create your views here.

@login_required
def roomView(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "live/room.html", {
        "project_id":project_id, 
        "project":project 
    })
