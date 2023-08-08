from django.contrib.auth.models import User
from django.contrib.auth import password_validation, authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import WorkSpace, Task, Asset


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "This username is not available. Please try using another username.")
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return email

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        temp_user = User(email=email, username=username)
        errors = []
        validators = password_validation.get_default_password_validators()
        for validator in validators:
            try:
                validator.validate(password, temp_user)
            except DjangoValidationError as error:
                errors.append(error)
                break
        if errors:
            raise serializers.ValidationError(errors[0].message)
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=1000)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['date_joined','username','email']


class WorkSpaceSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    class Meta:
        model = WorkSpace
        fields = [
            'name',
            'created_at',
            'members',
            'id'
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    workspaces = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'workspaces']

    def get_workspaces(self, user):
        workspace_queryset = WorkSpace.objects.filter(
            members=user
        )
        return WorkSpaceSerializer(workspace_queryset, many=True).data


class WorkSpaceCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class TaskCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name','description', 'deadline']

class TaskSerializer(serializers.ModelSerializer):
    assigned_user = MemberSerializer()

    class Meta:
        model = Task
        fields = ['name','description','status','deadline','assigned_user','id']

class TaskEditSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    id = serializers.IntegerField()
    deadline = serializers.DateTimeField(required=False)
    assigned_user = serializers.IntegerField(required=False)


class AssetSerializer(serializers.ModelSerializer):

    uploaded_by = MemberSerializer()
    class Meta:
        model = Asset
        fields = [
        'name',
        'description',
        'url',
        'uploaded_by',
        'uploaded_on',
        ]

class AssetCreationSerializer(serializers.Serializer):
    '''Serializer for uploading an asset'''
    file = serializers.ImageField()
    name = serializers.CharField()
    description = serializers.CharField()