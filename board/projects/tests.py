from django.test import TestCase
from django.urls import reverse 
from rest_framework import status 
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User 

from projects.models import Project, Task
from projects.api import serializers, views 

# Create your tests here.

########## Models Tests ##########

class ProjectModelTest(TestCase):

    @classmethod
    def setUpTestData(cls): 
        # create an user for the test 
        testuser = User.objects.create_user(
            username='testuser', password='testpass'
        ) 
        # create a Project object for the test 
        Project.objects.create(
            title = 'Test Project', 
            description = 'This is a test project', 
            created_by = testuser, 
            finish_date = '2023-03-31', 
            private = True 
        )

    def test_title_label(self):
        project = Project.objects.get(id = 1)
        field_label = project._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_created_by_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('created_by').verbose_name
        self.assertEqual(field_label, 'created by')

    def test_finish_date_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('finish_date').verbose_name
        self.assertEqual(field_label, 'finish date')

    def test_private_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('private').verbose_name
        self.assertEqual(field_label, 'private')

    def test_title_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_is_title_comma_username(self):
        project = Project.objects.get(id=1)
        expected_object_name = f'{project.title}, {project.created_by.username}'
        self.assertEqual(expected_object_name, str(project))


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # crea un utente per i test
        testuser = User.objects.create_user(
            username='testuser', password='testpass')

        # crea un oggetto Project per i test
        project = Project.objects.create(
            title='Test Project',
            description='This is a test project',
            created_by=testuser,
            finish_date='2023-03-31',
            private=True,
        )

        # crea un oggetto Task per i test
        Task.objects.create(
            title='Test Task',
            description='This is a test task',
            project=project,
            created_by=testuser,
            tags='test, task',
            progress='in progress',
            finish_date='2023-03-10',
        )

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_project_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('project').verbose_name
        self.assertEqual(field_label, 'project')

    def test_created_by_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('created_by').verbose_name
        self.assertEqual(field_label, 'created by')

    def test_tags_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('tags').verbose_name
        self.assertEqual(field_label, 'tags')

    def test_progress_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('progress').verbose_name
        self.assertEqual(field_label, 'progress')

    def test_finish_date_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('finish_date').verbose_name
        self.assertEqual(field_label, 'finish date')

    def test_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_is_title_comma_project(self):
        task = Task.objects.get(id=1)
        expected_object_name = f'{task.title}, {task.project.title}'
        self.assertEqual(expected_object_name, str(task))

##################################################

