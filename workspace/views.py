from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helpers.functions import format_serializer_errors
import workspace
from .models import WorkSpace, Task, Asset
from .serializers import (AssetSerializer, WorkSpaceCreationSerializer,TaskSerializer,
                           LoginSerializer, UserDetailSerializer,
                               SignUpSerializer, TaskCreationSerializer,
                                 WorkSpaceSerializer, TaskEditSerializer)

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
            workspace = WorkSpace.objects.create(
                name = f"{username}'s Workspace"
            )
            workspace.admins.add(user)
            workspace.members.add(user)
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
        return Response(data={"error": format_serializer_errors(data.errors)}, status=400)
        


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


class WorkSpaceCreationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = WorkSpaceCreationSerializer(data=request.data)
        if data.is_valid():
            name = data.validated_data.get("name")
            w_space = WorkSpace.objects.create(name=name)
            w_space.members.add(request.user)
            w_space.admins.add(request.user)
            return Response()
        return Response(data={"error": format_serializer_errors(data.errors)}, status=400)


class WorkSpaceTasks(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, workspace_id):
        workspace = WorkSpace.objects.filter(id=workspace_id).first()
        if workspace:
            tasks = workspace.task_set.all()
            data = TaskSerializer(tasks, many=True).data
            return Response(data=data)
        else:
            return Response(data={"error":"Invalid workspace"}, status=400)
        

class CreateTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, workspace_id):
        data = TaskCreationSerializer(data=request.data)
        if data.is_valid():
            workspace = WorkSpace.objects.filter(id=workspace_id).first()
            if workspace:
                Task.objects.create(
                    name=data.validated_data.get("name"),
                    deadline=data.validated_data.get("deadline"),
                    description=data.validated_data.get('description'),
                    workspace=workspace
                )
                return Response()
            else:
                return Response(data={"error":"Invalid workspace"}, status=400)
        return Response(data={"error": format_serializer_errors(data.errors)}, status=400)

    def put(self, request, workspace_id):
        data = TaskEditSerializer(data=request.data)
        if data.is_valid():
            vdata = data.validated_data
            name= vdata.get("name")
            description= vdata.get("description")
            status= vdata.get("status")
            id= vdata.get("id")
            deadline= vdata.get("deadline")
            assigned_user= vdata.get("assigned_user")
            user = None
            if assigned_user:
                user_qs = User.objects.filter(id=assigned_user).first()
                if not user_qs:
                    return Response(data={"error":"Invalid user"}, status=400)
                user = user_qs
            task = Task.objects.filter(id=id).first()
            if not task:
                return Response(data={"error":"Invalid task"}, status=400)
            task.name = name
            task.description = description
            task.status = status
            task.deadline = deadline or task.deadline
            task.assigned_user = user
            task.save()
            return Response()
        return Response(data={"error": format_serializer_errors(data.errors)}, status=400)
        
        

class WorkSpaceList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        workspaces = WorkSpace.objects.filter(
            members=request.user
        ).order_by('name')
        data = WorkSpaceSerializer(workspaces, many=True).data
        return Response(data=data)
    

class WorkSpaceAssetsListView(APIView):
    def get(self, request, workspace_id):
        workspace = WorkSpace.objects.filter(id=workspace_id).first()
        if workspace:
            assets = workspace.asset_set.all()
            data = AssetSerializer(assets, many=True).data
            return Response(data=data)
        else:
            return Response(data={"error":"Invalid workspace"}, status=400)
