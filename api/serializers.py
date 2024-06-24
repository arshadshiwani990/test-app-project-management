from rest_framework import serializers
from .models import Project, Task, ProjectUser

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_by', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'project', 'created_by', 'created_at']

class ProjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = ['user', 'project', 'permission']
