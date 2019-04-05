from django.urls import path
from . import views

app_name = 'omr'
urlpatterns = [
	path('signup/', views.signup, name='signup'),
	path('signup_complete/', views.signup_complete, name='signup_complete'),
	path('home/', views.home, name='home'),
	path('upload_files/', views.upload_files, name='upload_files'),
	path('<int:task_number>/delete_tasks/', views.delete_tasks, name='delete_tasks'),
]