from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message= models.TextField()
    response =models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_correct = models.BooleanField(default=None, null=True, blank=True)  # New field
    correct_file_path = models.TextField(null=True, blank=True)  # New field
    incorrect_file_path = models.TextField(null=True, blank=True)  # New field

    
    def __str__(self):
        return f"{self.user.username}: {self.message}"
    


