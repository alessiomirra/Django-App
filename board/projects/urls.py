from django.urls import path 
from projects import views 

##### 

urlpatterns = [
    path("projects/", views.ProjectListView.as_view(), name="list"), 
    path("projects/create/", views.ProjectCreateView.as_view(), name="create"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="detail"), 
    path("projects/<int:pk>/update/", views.ProjectUpdtateView.as_view(), name="edit"),
    path("projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="delete"),   
    path("projects/<int:pk>/create-task/", views.TaskCreateView.as_view(), name="create-task"),
    path("projects/<int:pk>/update-task/<int:task_pk>/", views.TaskUpdateView.as_view(), name="edit-task"),  
    path("projects/<int:pk>/join/", views.ProjectMembershipView.as_view(), name="join_project"), 
    path("projects/<int:pk>/leave/", views.ProjectMembershipDelete.as_view(), name="leave_project"), 
    path("projects/<int:project_id>/content/create/", views.ContentCreateView.as_view(), name="project_content_create"),
    path("projects/<int:project_id>/content/delete/<int:content_id>/", views.ContentDeleteView.as_view(), name="project_content_delete"),
    path("projects/<int:pk>/contents/", views.ProjectContentList.as_view(), name="project_content_list"),   
    path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task-details"), 
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="t-delete"), 
    path("comment/delete/<int:pk>/", views.CommentDeleteView.as_view(), name="comment-delete"), 
    path("permission_denied/", views.PermissionDeniedView.as_view(), name="permission_denied"), 
]
