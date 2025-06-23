from django.db import models
from django.contrib.auth.models import AbstractUser

class users(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)	
    

class Conversation(models.Model):
    participants = models.ManyToManyField(users)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Message(models.Model):
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	sender = models.ForeignKey(users, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
