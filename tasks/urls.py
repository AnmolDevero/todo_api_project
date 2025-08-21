from django.urls import path
from .views import TaskListCreateView,TaskDetailView

urlpatterns = [
    path('api/tasks/', TaskListCreateView.as_view(), name='task_list_create'),
    path('api/task/<int:id>/', TaskDetailView.as_view(), name='task_detail')
]