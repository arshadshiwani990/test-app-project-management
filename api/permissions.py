from rest_framework import permissions
from .models import ProjectUser

class IsProjectAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        project = Project.objects.get(pk=view.kwargs['pk'])
        user_permissions = ProjectUser.objects.filter(project=project, user=request.user).first()
        if request.method in permissions.SAFE_METHODS:
            return True
        return user_permissions and user_permissions.can_edit

class CanCreateDeleteEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        project = Project.objects.get(pk=view.kwargs['pk'])
        user_permissions = ProjectUser.objects.filter(project=project, user=request.user).first()
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return user_permissions and user_permissions.can_create
        if request.method == 'DELETE':
            return user_permissions and user_permissions.can_delete
        if request.method == 'PUT' or request.method == 'PATCH':
            return user_permissions and user_permissions.can_edit
        return False
