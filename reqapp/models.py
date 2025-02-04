from django.db import models
from django.contrib.auth.models import User

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request by {self.user.username} at {self.created_at}'