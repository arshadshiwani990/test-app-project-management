from rest_framework.permissions import BasePermission
from .models import Project,ProjectUser
class IsProjectCreator(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy', 'update', 'partial_update']:
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user

class HasProjectPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            project = Project.objects.get(pk=view.kwargs['project_pk'])
            return ProjectUser.objects.filter(user=request.user, project=project, permission='create').exists()
        return True

    def has_object_permission(self, request, view, obj):
        project = obj.project
        if view.action in ['update', 'partial_update']:
            return ProjectUser.objects.filter(user=request.user, project=project, permission='edit').exists()
        if view.action == 'destroy':
            return ProjectUser.objects.filter(user=request.user, project=project, permission='delete').exists()
        return True
