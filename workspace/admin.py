from django.contrib import admin

# Register your models here.
from .models import WorkSpace, Asset, Task

admin.site.register(WorkSpace)
admin.site.register(Asset)
admin.site.register(Task)
