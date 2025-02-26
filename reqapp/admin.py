from django.contrib import admin
from .models import Request, Device, Category, Audience, ClosedRequest, WrittenOffDevice

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'description', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('description', 'user__username', 'device__name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class AudienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ClosedRequestAdmin(admin.ModelAdmin):
    list_display = ('request', 'closed_at')
    search_fields = ('request__description', 'request__user__username')

class WrittenOffDeviceAdmin(admin.ModelAdmin):
    list_display = ('device', 'written_off_at')
    search_fields = ('device__name',)

admin.site.register(Audience, AudienceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Device)
admin.site.register(ClosedRequest, ClosedRequestAdmin)
admin.site.register(WrittenOffDevice, WrittenOffDeviceAdmin)