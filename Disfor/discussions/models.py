import uuid
from django.db import models

class Thread(models.Model):
    th_id       = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title       = models.CharField(max_length=200, null=False, blank=False)
    view_count  = models.IntegerField(default=0,null=False, blank=True)

    t_parent_id = models.ForeignKey(to='self', db_column='t_parent_id', null=True, blank=True, on_delete=models.CASCADE)
    # logic to prevent such cascade condition should be implemented but it shouldnt be restrictive

    user_id     = models.ForeignKey(to='users.Users', db_column='user_id', on_delete=models.CASCADE, null=False, blank=False)
    # the above is the user_id who creates the thread

    def __str__(self):
        return self.th_id
        
    class Meta:
        db_table = 'thread'


class Thread_has_parent_grp(models.Model):
    th_id   = models.OneToOneField(Thread, primary_key=True, db_column='th_id', on_delete=models.CASCADE, related_name='parent_grp')
    grp_id  = models.ForeignKey(to='groups.Group', db_column='grp_id', related_name='child_thread', on_delete=models.CASCADE, null=False, blank= False)
    # logic to prevent such cascade condition should be implemented but it shouldnt be restrictive

    def __str__(self):
        return '{} childof'.format(self.th_id)
        
    class Meta:
        db_table = 'thread_has_parent_grp'


class User_delete_thread(models.Model):
    th_id   = models.OneToOneField(Thread, primary_key=True, db_column='th_id', on_delete=models.DO_NOTHING, related_name='thread_deleted_by')
    user_id    = models.ForeignKey(to='users.Users', db_column='user_id', related_name = 'deleted_thread', on_delete=models.CASCADE, null=False, blank=False)


    def __str__(self):
        return '{} deletedby'.format(self.th_id)
        
    class Meta:
        db_table = 'user_delete_thread'
