from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Audience(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='devices')
    code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    audience = models.ForeignKey(Audience, on_delete=models.SET_NULL, blank=True, null=True, related_name='devices')

    def __str__(self):
        return self.name

class Request(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыта'),
        ('in_progress', 'В процессе'),
        ('closed', 'Закрыта'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request by {self.user.username} for {self.device.name if self.device else "No device"} at {self.created_at} - Status: {self.get_status_display()}'
    def set_status(self, new_status):
        self.status = new_status
        self.save()

        if new_status == 'closed':
            ClosedRequest.objects.create(request=self)

class ClosedRequest(models.Model):
    request = models.OneToOneField(Request, on_delete=models.CASCADE, related_name='closed_request')
    closed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Closed Request: {self.request} at {self.closed_at}'

class WrittenOffDevice(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name='written_off_device')
    written_off_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Written Off Device: {self.device} at {self.written_off_at}'