from django.contrib import admin
from .models import ToDoItem, ToDoGroup
# Register your models here.

admin.site.register(ToDoGroup)
admin.site.register(ToDoItem)

