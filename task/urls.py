from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', task_api),
    path('tasks/<int:id>', task_detail_api),
    path('bulk_tasks/', task_extra),
]
