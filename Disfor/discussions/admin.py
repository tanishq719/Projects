from django.contrib import admin
from .models import *
from .reply_models import *

my_another_models = [
    Thread, Thread_has_parent_grp, User_delete_thread,
    Reply, Likes, Dislikes, User_delete_reply, Image
]

admin.site.register(my_another_models)
