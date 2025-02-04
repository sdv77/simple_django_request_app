from django.contrib import admin
from .models import Request, Device

admin.site.register(Request)
admin.site.register(Device)