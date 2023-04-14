from django.urls import path  
from live import views 

urlpatterns = [ 
    path("<int:project_id>/", views.roomView, name="room"), 
]