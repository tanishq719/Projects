import uuid
from django.db import models

class Reply(models.Model):
    reply_id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creation_date   = models.DateField(auto_now_add=True) # doubtfull
    edit_date       = models.DateTimeField(auto_now = True) # doubtful
    like_count      = models.IntegerField(default=0,blank=True)
    dislike_count   = models.IntegerField(default=0,blank=True)
    reply_count     = models.IntegerField(default=0,blank=True)
    txt_body        = models.TextField(null=False, blank=False)

    r_parent_id     = models.ForeignKey('self',db_column='r_parent_id', null=True, blank=True, related_name='child_replies', on_delete=models.CASCADE)
    # logic to prevent such cascade condition should be implemented but it shouldnt be restrictive

    r_liked_by      = models.ManyToManyField('users.Users', related_name='liked_reply', through='Likes', blank=True)

    r_disliked_by   = models.ManyToManyField('users.Users', related_name='disliked_reply', through='Dislikes', blank=True)

    def __str__(self):
        return self.reply_id
        
    class Meta:
        db_table = 'reply'

    
class Likes(models.Model):
    user_id     = models.ForeignKey('users.Users', db_column='user_id', on_delete=models.CASCADE, related_name='liked', null=False, blank=False)
    reply_id    = models.ForeignKey(Reply, db_column='reply_id', on_delete=models.DO_NOTHING, related_name='liked_by',null=False, blank=False)

    def __str__(self):
        return '{} liked {}'.format(self.user_id,self.reply_id)
        
    class Meta:
        db_table = 'likes'
        unique_together = (('user_id','reply_id'))


class Dislikes(models.Model):
    user_id     = models.ForeignKey('users.Users', db_column='user_id', on_delete=models.CASCADE, related_name='disliked', null=False, blank=False)
    reply_id    = models.ForeignKey(Reply, db_column='reply_id', on_delete=models.DO_NOTHING, related_name='disliked_by',null=False, blank=False)

    def __str__(self):
        return '{} disliked {}'.format(self.user_id,self.reply_id)
        
    class Meta:
        db_table = 'dislikes'
        unique_together = (('user_id','reply_id'))


class User_delete_reply(models.Model):
    reply_id   = models.OneToOneField(Reply, primary_key=True, db_column='reply_id', on_delete=models.DO_NOTHING, related_name='reply_deleted_by')
    user_id    = models.ForeignKey(to='users.Users', db_column='user_id', related_name = 'deleted_reply', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return '{} deletedby {}'.format(self.reply_id, self.user_id)
        
    class Meta:
        db_table = 'user_delete_reply'


class Image(models.Model):
    img_id      = models.IntegerField(primary_key=True)
    link_to_img = models.CharField(max_length=100, null=False, blank=False)

    reply_id    = models.ForeignKey(Reply, db_column='reply_id', related_name='related_img', on_delete=models.CASCADE, blank=True, null=False)

    def __str__(self):
        return self.img_id

    class Meta:
        db_table = 'image'