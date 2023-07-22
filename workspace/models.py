from django.db import models
from django.contrib.auth.models import User

class TimeAwareModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

TASK_STATUSES = (
    ("PENDING", "PENDING"),
    ("IN PROGRESS", "IN PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("ARCHIVED", "ARCHIVED")
)

class WorkSpace(TimeAwareModel):
    name = models.CharField(max_length=100)
    admins = models.ManyToManyField(User, blank=True,related_name="admins")
    created_at = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, blank=True, related_name="members")

    def __str__(self):
        return self.name
    
class Task(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1000, choices=TASK_STATUSES)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    deadline = models.DateTimeField(blank=True, null=True)
    assigned_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    

class Asset(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    file = models.FileField()

    def __str__(self):
        return self.name
    