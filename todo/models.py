from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_todos', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_todos', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title