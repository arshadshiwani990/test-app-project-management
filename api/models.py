from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProjectUser(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'View'),
        ('create', 'Create'),
        ('edit', 'Edit'),
        ('delete', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    permission = models.CharField(max_length=6, choices=PERMISSION_CHOICES, default='view')

    class Meta:
        unique_together = ('user', 'project', 'permission')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.permission}"