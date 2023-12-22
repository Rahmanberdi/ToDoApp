
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ToDoGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.group_title

class ToDoItem(models.Model):
    title = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    group = models.ForeignKey("ToDoGroup",on_delete=models.CASCADE, related_name='item')

    def save(self, *args, **kwargs):
        is_new_item = not self.pk  # Check if it's a new item
        super().save(*args, **kwargs)
        # Update the TodoGroup's updated_date when a TodoItem is created or updated
        if is_new_item or self.updated_date > self.group.updated_at:
            self.group.updated_date = self.updated_date
            self.group.save()

    def __str__(self):
        return self.title
