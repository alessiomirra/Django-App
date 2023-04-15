from django.shortcuts import get_object_or_404, redirect  
from django.views.generic.base import View 
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.base import TemplateView 
from django.urls import reverse_lazy 
from projects.models import Project, Task, Content, Comment, ProjectMembership 
from django.contrib.auth.models import User 
from projects.forms import CommentModelForm
from core.utils import get_current_date

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from live.models import Notification  

# Create your views here.

class OwnerMixin: 
    def get_queryset(self): 
        qs = super().get_queryset()
        return qs.filter(created_by = self.request.user).order_by("-id")

class OwnerEditMixin: 
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class OwnerProjectMixin(LoginRequiredMixin,OwnerMixin):
    model = Project 
    fields = ["title","description","finish_date","private"]
    success_url = reverse_lazy("list")

class OwnerProjectEditMixin(OwnerProjectMixin, OwnerEditMixin):
    template_name = "projects/project_form.html"

class TaskEditMixin(LoginRequiredMixin):
    model = Task 
    fields = ["title","description","tags","progress","finish_date"]
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        project_id = self.kwargs.get("pk")
        project = Project.objects.get(id = project_id)
        form.instance.project = project 
        form.instance.created_by = self.request.user 
        return super().form_valid(form)  

    def get_context_data(self, **kwargs):
        project_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(id = project_id)
        return context 

    def get_success_url(self): 
        project_id = self.kwargs.get('pk')
        success_url = reverse_lazy('detail', args=[project_id])
        return success_url  


################ Project Views ################

class ProjectListView(OwnerProjectMixin, ListView):
    # This generic views give an "object_list" list containing all the objects 
    template_name = 'projects/projects_list.html' 

    def get_queryset(self):
        return super().get_queryset().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = get_current_date()
        return context 


class ProjectDetailView(DetailView):
    model = Project 
    template_name = "projects/project_detail.html"  

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.private and obj.created_by != self.request.user: 
           raise PermissionDenied 
        return obj  

    def dispatch(self, request, *args, **kwargs):
        try: 
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            return redirect("permission_denied")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentModelForm()
        # get project's followers
        users = User.objects.filter(followed_projects__project = self.get_object())
        context["followers"] = users 
        return context 

    def post(self, request, *args, **kwargs):
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_by = request.user 
            comment.project = self.get_object()
            comment.save()
            return redirect("detail", pk=self.get_object().pk)
        return self.get(request, *args, **kwargs)

class ProjectCreateView(OwnerProjectEditMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)

        # send notification
        channel_layer = get_channel_layer()
        message = f"{self.request.user} has created a new project: '{self.object.title}'. Check project's list!"
        async_to_sync(channel_layer.group_send)(
            'notifications', 
            {
                "type": "send_notification", 
                "message": message,
            }   
        )

        # create the new Notification 
        new_notification = Notification.objects.create(
            project = self.object, 
            message = message, 
            user = self.request.user 
        )

        return response 

class ProjectUpdtateView(OwnerProjectEditMixin, UpdateView):
    pass 

class ProjectDeleteView(OwnerProjectMixin, DeleteView):
    template_name = "projects/project_delete.html"

#############################################

############### Task Views ##################

class TaskCreateView(TaskEditMixin,CreateView):
    pass 


class TaskUpdateView(TaskEditMixin, UpdateView):
    pk_url_kwarg = "task_pk"

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task 
    template_name = "tasks/task_detail.html"


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task 
    template_name = "tasks/task_delete.html"

    def get_success_url(self): 
        success_url = reverse_lazy("detail", kwargs={"pk":self.object.project.pk})
        return success_url 
 

#############################################

############### Content Views ##################
class ContentCreateView(LoginRequiredMixin, CreateView):
    model = Content 
    fields = ["title","file"]
    template_name = "content/content_form.html"

    def form_valid(self, form):
        project_id = self.kwargs.get("project_id")
        project = get_object_or_404(Project, id=project_id)
        form.instance.project = project 
        form.instance.created_by = self.request.user 
        return super().form_valid(form)  

    def get_success_url(self): 
        project_id = self.kwargs.get('project_id')
        success_url = reverse_lazy('project_content_list', args=[project_id])
        return success_url  

class ContentDeleteView(LoginRequiredMixin, DeleteView):
    model = Content 
    pk_url_kwarg = "content_id"
    template_name = "content/content_delete.html"

    def get_success_url(self): 
        project_id = self.kwargs.get('project_id')
        success_url = reverse_lazy('project_content_list', args=[project_id])
        return success_url   


class ProjectContentList(LoginRequiredMixin, ListView):
    model = Content 
    template_name = "content/content_list.html"

    def get_queryset(self):
        project_id = self.kwargs.get('pk')
        return Content.objects.filter(project__id = project_id)

    def get_context_data(self, **kwargs):
        project_id = self.kwargs.get("pk")
        context = super().get_context_data(**kwargs)
        context["project"] = Project.objects.get(id = project_id)
        return context 


################################################

############### Comment Views ##################

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment 

    def get_success_url(self):
        success_url = reverse_lazy("detail", kwargs={"pk":self.get_object().project.pk})
        return success_url

    def get_object(self, queryset):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied 
        return obj  

    def dispatch(self, request, *args, **kwargs):
        try: 
            return super().dispatch(request, *args, **kwargs) 
        except PermissionDenied:
            return redirect("permission_denied")

################################################

############### Enroll in Project Views ##################

class ProjectMembershipView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        project_id = self.kwargs.get("pk")
        project = Project.objects.get(id = project_id)
        user = request.user   
        membership = ProjectMembership.objects.create(
            project = project, 
            user = user
        )
        return redirect('detail', pk=project_id)

class ProjectMembershipDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        project_id = self.kwargs.get("pk")
        project = Project.objects.get(id = project_id)
        user = request.user 
        membership = ProjectMembership.objects.filter(
            project = project, 
            user = user, 
        ) 
        if membership: 
            membership.delete()
        return redirect('detail', pk=project_id)

################################################

class PermissionDeniedView(TemplateView):
    template_name = "permission_denied.html" 