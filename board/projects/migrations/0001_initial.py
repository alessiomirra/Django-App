# Generated by Django 4.1.7 on 2023-03-29 15:33

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
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('finish_date', models.DateField(blank=True, null=True)),
                ('private', models.BooleanField(default=False)),
                ('progress', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('tags', models.CharField(blank=True, max_length=40, null=True)),
                ('progress', models.CharField(blank=True, choices=[('in progress', 'in progress'), ('completed', 'completed')], default='in progress', max_length=40, null=True)),
                ('finish_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
