from rest_framework import generics 
from projects.models import Project, Task, Content, Comment  
from projects.api.serializers import ProjectSerializer, TaskSerializer, ContentSerializer, CommentSerializer 
from projects.api import permissions 

####### 

class ProjectsListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer 

class ProjectDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer 
    permission_classes = [permissions.IsAuthorOrReadOnly]

class TasksListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    permission_classes = [permissions.CheckTaskPermission]

class TasksForProject(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 

    def get_queryset(self):
        project_id = self.kwargs.get('pk')
        return Task.objects.filter(project__id = project_id)

class ContentListAPIView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer 

class ContentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer 
    permission_classes = [permissions.CheckAuthorPermission]

class ContentsForProject(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("pk")
        return Content.objects.filter(project__id = project_id)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.CheckAuthorPermission]

class CommentsForProjectAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 

    def get_queryset(self):
        project_id = self.kwargs.get("pk")
        return Content.objects.filter(project__id = project_id)