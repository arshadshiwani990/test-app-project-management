from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, ProjectUserViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'projects/(?P<project_pk>\d+)/tasks', TaskViewSet, basename='task')
router.register(r'project-users', ProjectUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
