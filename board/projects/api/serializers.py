from rest_framework import serializers 
from projects.models import Project, Task, Content, Comment  

######### 

class TaskSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)
    finish_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task 
        fields = "__all__"

    def get_date(self, instance):
        return instance.date.strftime("%B %d, %Y")

    def get_finish_date(self, instance):
        if instance.finish_date is not None:
            return instance.finish_date.strftime("%B %d, %Y")
        else: 
            return ""


class ProjectSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)
    finish_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project 
        fields = "__all__"

    def get_date(self, instance):
        return instance.date.strftime("%B %d, %Y")

    def get_finish_date(self, instance):
        if instance.finish_date is not None:
            return instance.finish_date.strftime("%B %d, %Y")
        else: 
            return ""

class ContentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Content 
        fields = "__all__" 

    def get_date(self, instance):
        return instance.date.strftime("%B %d, %Y")


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment 
        fields = "__all__"

    def get_date(self, instance):
        return instance.date.strftime("%B %d, %Y")