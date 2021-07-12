from rest_framework import serializers

from apps.authentications.models import User
from apps.authentications.serializers import UserSerializer
from apps.tasks.models import Task


class TaskListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'summary', 'user', 'performed_at')
        read_only_fields = ('id',)

    def to_internal_value(self, data):
        self.fields['user'] = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.all()
        )

        return super().to_internal_value(data)


class TaskDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'summary', 'user', 'performed_at')
        read_only_fields = ('id', 'summary', 'user')
