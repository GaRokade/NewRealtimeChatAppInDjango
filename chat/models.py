from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content}"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_active = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username
class User(models.Model):
    username = models.CharField(max_length=100)
    # Other fields
