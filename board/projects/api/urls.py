from django.urls import path 
from rest_framework import permissions 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from projects.api import views 

###### 

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('projects-api', views.ProjectsListAPIView.as_view(), name="projects-list"),
    path('projects-api/<int:pk>/', views.ProjectDetailsAPIView.as_view(), name="project-details"),
    path('projects-api/<int:pk>/tasks/', views.TasksForProject.as_view(), name="tasks-for-project"),
    path("projects-api/<int:pk>/contents/", views.ContentsForProject.as_view(), name="contents-for-project"), 
    path("projects-api/<int:pk>/comments/", views.CommentsForProjectAPIView.as_view(), name="comments-for-project"), 
    path('tasks-api/', views.TasksListAPIView.as_view(), name="tasks-list"),
    path('tasks-api/<int:pk>/', views.TaskDetailAPIView.as_view(), name="task-detail"), 
    path('content-api/', views.ContentListAPIView.as_view(), name='c-list'),
    path('content-api/<int:pk>/', views.ContentDetailAPIView.as_view(), name="c-detail"),  
    path('comments-api/', views.CommentListAPIView.as_view(), name="comm-list"),
    path('comments-api/create/', views.CommentCreateAPIView.as_view(), name="comm-create"), 
    path('comments-api/<int:pk>/', views.CommentDetailAPIView.as_view(), name="comm-detail"),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]