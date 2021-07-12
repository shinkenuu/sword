from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views as auth_token_views

from apps.tasks.views import TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', auth_token_views.obtain_auth_token, name='api-token-auth'),
    path('tasks', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
]
