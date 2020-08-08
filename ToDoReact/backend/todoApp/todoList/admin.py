from django.contrib import admin
from .models import TodoList, TodoItem, MyUser

# Register your models here.
model_tables = [TodoItem,TodoList, MyUser]
admin.site.register(model_tables)