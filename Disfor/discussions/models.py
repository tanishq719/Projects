import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField

class Thread(models.Model):
    th_id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title       = models.CharField(max_length=200, null=False, blank=False)
    view_count  = models.IntegerField(default=0,null=False, blank=True)
    
    body        = models.OneToOneField('discussions.Reply', db_column='body', related_name = 'attached_to', on_delete=models.CASCADE, null=False, blank=False)

    t_parent_t = models.ForeignKey(to='self', db_column='t_parent_t', related_name='child_thread', null=True, blank=True, on_delete=models.CASCADE)
    # Thread will never be deleted, at max it can be closed, but still data is always their

    t_creator    = models.ForeignKey(to='users.Users', db_column='t_creator',related_name='created_thread', on_delete=models.SET_NULL, null=True, blank=True)
    # the above is the user_id who creates the thread

    t_parent_grp    = models.ForeignKey(to='groups.Group', db_column='t_parent_grp', related_name='child_thread', on_delete=models.SET_NULL, null=True, blank= True)

    def __str__(self):
        return self.th_id
        
    class Meta:
        db_table = 'thread'


# class Thread_has_parent_grp(models.Model):
#     th_id   = models.OneToOneField(Thread, primary_key=True, db_column='th_id', on_delete=models.CASCADE, related_name='parent_grp')
#     grp_id  = models.ForeignKey(to='groups.Group', db_column='grp_id', related_name='child_thread', on_delete=models.CASCADE, null=False, blank= False)
#     # logic to prevent such cascade condition should be implemented but it shouldnt be restrictive

#     def __str__(self):
#         return '{} childof'.format(self.th_id)
        
#     class Meta:
#         db_table = 'thread_has_parent_grp'


class Grp_closes_thread(models.Model):
    th_id   = models.OneToOneField(Thread, primary_key=True, db_column='th_id', on_delete=models.DO_NOTHING, related_name='thread_closed_by')
    grp_id    = models.ForeignKey(to='groups.Group', db_column='grp_id', related_name = 'closed_thread', on_delete=models.SET_NULL, null=True, blank=True)
    reason    = JSONField()

    def __str__(self):
        return '{} closeedby {}'.format(self.th_id, self.grp_id)
        
    class Meta:
        db_table = 'group_close_thread'
