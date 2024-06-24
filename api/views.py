from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Task, ProjectUser
from .serializers import ProjectSerializer, TaskSerializer, ProjectUserSerializer
from .permissions import IsProjectCreator, HasProjectPermission
from rest_framework.response import Response
from rest_framework import viewsets, status
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectCreator]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, HasProjectPermission]

    def get_queryset(self):
        return Task.objects.filter(project__id=self.kwargs['project_pk'], is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()



from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ProjectUser
from .serializers import ProjectUserSerializer
from .permissions import IsProjectCreator

class ProjectUserViewSet(viewsets.ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserSerializer
    permission_classes = [IsAuthenticated, IsProjectCreator]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        
        project = serializer.validated_data['project']
        if request.user != project.created_by:
            return Response({"error": "Only the project owner can assign permissions."},
                            status=status.HTTP_403_FORBIDDEN)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
