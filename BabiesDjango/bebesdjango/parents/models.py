from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Parent(User):
	name=models.CharField(max_length=100, null=False)

	def __str__(self):
		return self.name
