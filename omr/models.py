from django.db import models

# Create your models here.
class Home(models.Model):
	number = models.IntegerField(default = 0)
	course_code = models.CharField(max_length=200)
	course_name = models.CharField(max_length=200)
	date = models.DateTimeField('date published')
	status = models.CharField(max_length=200)
	remarks = models.CharField(max_length=200)
