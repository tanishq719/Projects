from django.contrib import admin
from users.models import Users, Notification, User_block_user

model_tables = [Users,Notification,User_block_user]
admin.site.register(model_tables)