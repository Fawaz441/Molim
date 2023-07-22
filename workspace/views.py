from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.functions import format_serializer_errors
from .models import WorkSpace, Task, Asset
from .serializers import WorkSpaceSerializer, LoginSerializer, UserDetailSerializer,  SignUpSerializer

# Create your views here.


class SignUpAPIView(APIView):
    def post(self, request):
        data = SignUpSerializer(data=request.data)
        if data.is_valid():
            vdata = data.validated_data
            username = vdata.get("username")
            email = vdata.get("email")
            password = vdata.get("password")
            user = User.objects.create(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
            data = UserDetailSerializer(user).data
            return Response(data=data)
        return Response(data={"error": format_serializer_errors(data.errors)}, status=400)


class LoginAPIView(APIView):
    def post(self, request):
        data = LoginSerializer(data=request.data)
        if data.is_valid():
            vdata = data.validated_data
            email = vdata.get("email")
            password = vdata.get("password")
            user = User.objects.filter(email__iexact=email).first()
            if not user:
                return Response(data={"error": "Incorrect email or password"}, status=400)
            if not user.check_password(password):
                return Response(data={"error": "Incorrect email or password"}, status=400)
            token, _ = Token.objects.get_or_create(user=user)
            data = UserDetailSerializer(user).data
            data.update(token=token.key)
            return Response(data=data)


class DashboardOverview(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_user=user)
        overdue_tasks = tasks.filter(
            deadline__lt=timezone.now()).exclude(status="COMPLETED")
        completed_tasks = tasks.filter(status="COMPLETED")
        uncompleted_tasks = tasks.filter(status__in=[
            "PENDING",
            "IN PROGRESS"
        ], deadline__gt=timezone.now())

        data = {
            "total_tasks": tasks.count(),
            "ovedue_tasks": overdue_tasks.count(),
            "completed_tasks": completed_tasks.count(),
            "uncompleted_tasks": uncompleted_tasks.count()
        }
        return Response(data=data)
