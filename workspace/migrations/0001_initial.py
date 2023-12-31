# Generated by Django 4.2.3 on 2023-07-22 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('admins', models.ManyToManyField(blank=True, related_name='admins', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('IN PROGRESS', 'IN PROGRESS'), ('COMPLETED', 'COMPLETED'), ('ARCHIVED', 'ARCHIVED')], max_length=1000)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('assigned_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.workspace')),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True, null=True)),
                ('file', models.FileField(upload_to='')),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspace.workspace')),
            ],
        ),
    ]
