from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'assigned_to')
    search_fields = ('title', 'description')
    list_filter = ('created_by', 'assigned_to')