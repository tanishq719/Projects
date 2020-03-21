from django.db import models

class Tag(models.Model):
    tag_id      = models.IntegerField(primary_key=True)
    tag_name    = models.CharField(max_length=50, unique=True)

    g_has_t     = models.ManyToManyField('groups.Group',related_name='grp_has_tag', through='Group_has_tag', blank=True)

    th_has_t    = models.ManyToManyField('discussions.Thread', related_name='thread_has_tag', through='Thread_has_tag', blank=True)

    def __str__(self):
        return self.tag_name

    class Meta:
        db_table = 'tag'

    
class Group_has_tag(models.Model):
    grp_id  = models.ForeignKey(to='groups.Group', db_column='grp_id', related_name='tagged_grp', on_delete=models.CASCADE, null=False, blank= False)
    tag_id  = models.ForeignKey(to=Tag, db_column='tag_id', related_name='grp_tag', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} having {}'.format(self.grp_id, self.tag_id)

    class Meta:
        db_table = 'group_has_tag'
        unique_together = (('grp_id','tag_id'))


class Thread_has_tag(models.Model):
    th_id  = models.ForeignKey(to='discussions.Thread', db_column='th_id', related_name='tagged_thread', on_delete=models.CASCADE, null=False, blank= False)
    tag_id  = models.ForeignKey(to=Tag, db_column='tag_id', related_name='thread_tag', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} having {}'.format(self.th_id, self.tag_id)

    class Meta:
        db_table = 'thread_has_tag'
        unique_together = (('th_id','tag_id'))
