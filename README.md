# PROJECT BOARD 

This is a Django application providing the necessary API for a project management board application. 
The application has the following functionality: 
- User authentication using an external Oauth2-OpenID provider 
- CRUD Project API 
- CRUD Task API 
- Extras functionality

## 1. User Authentication 

There're two possible ways to enroll/login in the app: 
1. Using the django.contrib.auth endpoints, so the django default authentication
2. Using the external Google provider

Both the Django's authentication endpoints and the logic for the exteral provider login have been provided by using the external package django-allauth

## 2. CRUD Project API 

The base Project model has the following fields: 
- title 
- description 
- created_by 
- finish_date
- private
- progress 

The "progress" field is automatically uploaded. I've defined the following model method inside the Project model: 

```python
def update_progress(self):
    tasks = self.task_set.all()
    if tasks.count() > 0:
        completed_tasks = tasks.filter(progress = "completed")
        self.progress = int((completed_tasks.count() / tasks.count()) * 100 )
    else: 
        self.progress = 0 
    self.save()
```

This method retrieves all tasks related to a field, checks the number of tasks completed, then it calculates the progress value as a percentage. 
The "progress" field for Project model is automatically uploaded. 

The views for this model have been written using class-based views 

The Project's API view have been written using Django Rest Framework's generics API views 

## 3. CRUD Task API 

The base Task model has the following fields: 
- title 
- description
- project 
- created_by 
- date 
- tags 
- progress 
- finish_date 

The "progress" field for Task is uploaded by the user. 
The model is the following: 

```python
class Task(models.Model):
    PROGRESS_CHOISES = (
        ("in progress", "in progress"), 
        ("completed", "completed"), 
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    date = models.DateField(auto_now_add=True)
    tags = models.CharField(max_length=40, blank=True, null=True)
    progress = models.CharField(max_length=40, choices=PROGRESS_CHOISES, default="in progress", blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.project.title}"

    def get_absolute_url(self):
        return reverse("task-details", kwargs={"pk":self.pk})

    def check_is_completed(self):
        return self.progress == "completed"
```

## 4. Extras Functionalities

- Content For Projects

The user'll be able to add content, such as files, for a Project. 

```python
class Content(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_contents")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_contents")
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='files')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  
```

- Comment System 
I've created a comment section for each project

```python
class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_comments")
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"Comment by {self.created_by.username} for {self.project.title}"
```


### How to set up the project to run in your local machine? 
Download the code to your PC, unpack the ZIP and move it inside the folder
Create a new Python Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment and install all the Python/Django dependencies: 

```bash
source venv/bin/activate
pip install -m ./requirements.txt
```

Run Django Development Server 

```python
python manage.py runserver 
```

### Possible features

1. Notification System
It would be a good idea to create a notification system to inform the project's creator when a project is at the 100% progress or when a project is near to the finish_date

2. Chat System 
Create a Chat Room for each project 



##### version 2