from django.contrib import admin
from .models import Request, Device

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'description', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('description', 'user__username', 'device__name')

admin.site.register(Request, RequestAdmin)
admin.site.register(Device)