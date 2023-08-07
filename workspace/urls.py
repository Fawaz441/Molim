from django.urls import path
from .views import (SignUpAPIView, LoginAPIView, DashboardOverview, WorkSpaceAssetsListView,
                     WorkSpaceCreationView,WorkSpaceTasks, WorkSpaceList,
                     CreateTask)

urlpatterns = [
    path("login",LoginAPIView.as_view()),
    path("signup",SignUpAPIView.as_view()),
    path("tasks-overview",DashboardOverview.as_view()),
    path("create-workspace",WorkSpaceCreationView.as_view()),
    path("workspaces/<int:workspace_id>/tasks", WorkSpaceTasks.as_view()),
    path("workspaces", WorkSpaceList.as_view()),
    path("workspaces/<int:workspace_id>/tasks/create", CreateTask.as_view()),
    path("workspaces/<int:workspace_id>/assets",WorkSpaceAssetsListView.as_view())
]