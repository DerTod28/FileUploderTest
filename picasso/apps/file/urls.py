from django.urls import path
from .views import FileUploadView, file_list, check_task_status

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', file_list, name='file-list'),
    path('check-task-status/<str:task_id>/', check_task_status, name='check-task-status'),
]
