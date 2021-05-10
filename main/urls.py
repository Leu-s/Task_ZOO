from django.urls import path
from .views import index
from .views import task_info
from .views import zoo_view
from .views import CreateZooView
from .views import update_changes


urlpatterns = [
    path('', index, name='index'),
    path('info/', task_info, name='task-info'),
    path('zoo/<int:pk>/', zoo_view, name='zoo'),
    path('create/', CreateZooView.as_view(), name='create-zoo'),
    path('update/', update_changes, name='zoo-update'),
]
