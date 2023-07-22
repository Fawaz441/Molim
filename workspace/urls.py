from django.urls import path
from .views import SignUpAPIView, LoginAPIView, DashboardOverview

urlpatterns = [
    path("login",LoginAPIView.as_view()),
    path("signup",SignUpAPIView.as_view()),
    path("tasks-overview",DashboardOverview.as_view())
]