from django.contrib import admin
from groups.models import *
from groups.tag_models import *

my_models = [
    Group, Group_criteria, Has_members, Has_followers,
    Grp_deletes_grp,Grp_blocks_user,Grp_blocks_grp,
    Tag, Group_has_tag, Thread_has_tag
    ]

admin.site.register(my_models)