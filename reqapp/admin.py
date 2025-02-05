from django.contrib import admin
from .models import Request, Device, Category

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'device', 'description', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('description', 'user__username', 'device__name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Device)