from django.views.generic.list import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.cache import cache 

from projects.models import Project
from core.utils import get_current_date
### 


class Homepage(LoginRequiredMixin,ListView):
    model = Project 
    template_name = 'homepage.html'

    def get_queryset(self): 
        qs = super().get_queryset()
        return qs.filter(private = False).order_by('-date') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = get_current_date()
        return context 
        
    '''
    def get_projects_number(self, **kwargs):
        projects_number = cache.get("projects_number")
        if not projects_number: 
            projects_number = Project.objects.all().count()
            cache.set('projects_number', projects_number)
    '''
