from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.authentications.permissions import IsOwner, IsManager
from apps.tasks.models import Task
from apps.tasks.serializers import TaskDetailSerializer, TaskListSerializer


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskListSerializer

    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.user.is_manager:
            return Task.objects.all()

        return Task.objects.filter(user=self.request.user).all()

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]

        if self.request.method in ('POST'):
            self.permission_classes += [IsManager]

        return super().get_permissions()


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer

    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        if self.request.user.is_manager:
            return Task.objects.all()

        return Task.objects.filter(user=self.request.user).all()

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]

        if self.request.method in ('PUT', 'PATCH'):
            self.permission_classes += [IsOwner]

        elif self.request.method == 'DELETE':
            self.permission_classes += [IsManager]

        return super().get_permissions()
