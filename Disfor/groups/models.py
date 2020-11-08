import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from PIL import Image

class Group(models.Model):

    CHOICES = [
        ('PUB', 'Public'),
        ('PRI', 'Private')
    ]
    grp_id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grp_name            = models.CharField(max_length=100, blank=False, null=False)# it should be title and of 20 length
    grp_creation_date   = models.DateField(auto_now_add=True)
    access_type         = models.CharField(max_length=3,null=False,blank=False,choices=CHOICES,default='PUB')
    description         = models.TextField(null=False,blank=False)
    reputation          = models.IntegerField(default=0,blank=True)
    subscriber_count    = models.IntegerField(default=0,blank=True)
    notification_q      = JSONField()
    dp                  = models.ImageField(upload_to='profile_image', blank=False, default='user.png')

    g_parent_id         = models.ForeignKey('self', db_column='g_parent_id', on_delete=models.CASCADE, blank= False,null=False)
    grp_admin           = models.ForeignKey('users.Users', db_column='grp_admin', related_name= 'grp_admin',on_delete=models.PROTECT, blank=False, null=False)
    # Prevent deletion of the referenced object by raising ProtectedError, a subclass of django.db.IntegrityError.

    g_members_u         = models.ManyToManyField('users.Users',related_name='owned_grp', through='Has_members', blank=True)

    g_followers_u       = models.ManyToManyField('users.Users',related_name='subscribed_to', through='Has_followers', blank=True)

    g_blocks_u          = models.ManyToManyField('users.Users',related_name='blocked_by_grp', through='Grp_blocks_user', blank=True)

    g_blocks_g          = models.ManyToManyField('self',related_name='blocked_by_grp', through='Grp_blocks_grp', blank=True)

    g_deletes_g         = models.ManyToManyField('self',related_name='deleted_by_grp', through='Grp_deletes_grp', blank=True)


    def __str__(self):
        return self.grp_name
        
    class Meta:
        db_table = 'group'

    def __unicode__(self):
        return '{0}'.format(self.dp)

    def save(self):
        if not self.dp:
            return

        super(Group, self).save()
        image = Image.open(self.dp)
        (width, height) = image.size
        size = ( 200, 200)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.dp.path)


class Group_criteria(models.Model):
    # criteria is for 2nd degree reply and group creation
    # separate table is created as only public group will have requirement for criteria 
    grp_id          = models.ForeignKey(Group, to_field='grp_id', db_column = 'grp_id', primary_key=True, related_name='see_criteria', on_delete=models.CASCADE)
    criteria_value  = models.CharField(max_length=20, null=False, blank=False)  # format : reply_criteria, group_forming_criteria
                                                                                # ex: 100, 1000

    def __str__(self):
        return '{} criteria'.format(self.grp_id)

    class Meta:
        db_table = 'group_criteria'


class Has_members(models.Model):
    grp_id      = models.ForeignKey(to=Group, db_column='grp_id', related_name='grp_members', on_delete=models.CASCADE, null=True, blank= False)
    user_id    = models.ForeignKey(to='users.Users', db_column='user_id', related_name = 'member_user_id', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{} members'.format(self.grp_id)

    class Meta:
        db_table = 'has_members'
        unique_together = (('grp_id','user_id'))


class Has_followers(models.Model):

    grp_id      = models.ForeignKey(to=Group, db_column='grp_id', related_name='grp_followers', on_delete=models.CASCADE, null=True, blank= False)
    user_id     = models.ForeignKey(to='users.Users', db_column='user_id', related_name = 'follower_user_id', on_delete=models.SET_NULL, null=True, blank=False)
    yes_notify      = models.CharField(max_length=1, null=False, blank=False)
    notification_q  = JSONField()

    def __str__(self):
        return '{} followers'.format(self.grp_id)

    class Meta:
        db_table = 'has_followers'
        unique_together = (('grp_id','user_id'))


class Grp_blocks_user(models.Model):
    grp_id      = models.ForeignKey(to=Group, db_column='grp_id', related_name='grp_blocked_usr', on_delete=models.CASCADE, null=False, blank= False)
    user_id     = models.ForeignKey(to='users.Users', db_column='user_id', related_name = 'blocked_user_id', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '{} blocked {}'.format(self.grp_id,self.user_id)

    class Meta:
        db_table = 'grp_blocks_user'
        unique_together = (('grp_id','user_id'))


class Grp_blocks_grp(models.Model):
    grp_id_from     = models.ForeignKey(to=Group, db_column='grp_id_from', related_name='grp_blocked_grp', on_delete=models.CASCADE, null=False, blank= False)
    grp_id_to       = models.ForeignKey(to=Group, db_column='grp_id_to', related_name='blocked_grp_id', on_delete=models.SET_NULL, null=True, blank= True)

    def __str__(self):
        return '{} blocked {}'.format(self.grp_id_from,self.grp_id_to)

    class Meta:
        db_table = 'grp_blocks_grp'
        unique_together = (('grp_id_from','grp_id_to'))


class Grp_deletes_grp(models.Model):
    grp_id_from     = models.ForeignKey(to=Group, db_column='grp_id_from', related_name='grp_deleted_grp', on_delete=models.CASCADE, null=False, blank= False)
    grp_id_to       = models.ForeignKey(to=Group, db_column='grp_id_to', related_name='deleted_grp_id', on_delete=models.DO_NOTHING, null=False, blank= False)
    reason          = JSONField()

    def __str__(self):
        return '{} deleted {}'.format(self.grp_id_from,self.grp_id_to)

    class Meta:
        db_table = 'grp_deleted_grp'
        unique_together = (('grp_id_from','grp_id_to'))
