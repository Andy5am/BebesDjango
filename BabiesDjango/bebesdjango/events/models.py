from django.db import models
from datetime import datetime

# Create your models here.
class Event(models.Model):
	event_type=models.CharField(max_length=100, null = False)
	date=models.DateTimeField(default = datetime.now,blank=True)
	description= models.CharField(max_length=500, null=True)
	baby=models.ForeignKey(
		'babies.Baby',
		null=False,
		on_delete=models.CASCADE)

	def __str__(self):
		return self.event_type
