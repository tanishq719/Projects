from django.contrib import admin
from .models import *
from .reply_models import *

my_another_models = [
    Thread,  Grp_closes_thread,
    Reply, Likes, Dislikes, User_delete_reply,
    Group_closes_reply,Image
]

admin.site.register(my_another_models)
