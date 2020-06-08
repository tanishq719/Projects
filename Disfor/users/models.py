from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Users(models.Model):
    username            = models.CharField(max_length = 25, primary_key = True)
    first_name          = models.CharField(max_length = 25, null=False, blank=False)
    last_name           = models.CharField(max_length = 25, null=False, blank=False)
    join_date           = models.DateField(auto_now_add=True) # doubtfull
    email               = models.EmailField(null=False, blank=False, unique=True, max_length=60)
    last_active_date    = models.DateTimeField(auto_now = True) # doubtful
    reputation          = models.IntegerField(default=0,blank=True)
    password            = models.CharField(max_length=100,null=False, blank=False)
    like_count          = models.IntegerField(default=0,blank=True)
    dislike_count       = models.IntegerField(default=0,blank=True)
    reply_count         = models.IntegerField(default=0,blank=True)
    # discription about user
    description         = models.CharField(max_length = 200, default = "null",null=False, blank=False)
    dp                  = models.ImageField(upload_to='profile_image', blank=True)

    u_relate_u          = models.ManyToManyField('self',through='User_block_user', blank=True, symmetrical=False)
    #u1.u_relate_u.add(u2)
    #u1.u_relate_u.create(atributes....)
    # user_block_user     = models.ManyToManyField('self',related_name='from_user',blank=True, symmetrical=False)
    #u1.user_block_user.add(u2)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
    
    # check_password(password, encoded)
    # make_password(password, salt=None, hasher='default')
    # is_password_usable(encoded_password)


class User_block_user(models.Model):
    #can assign values in username_1 as ra1.username_1 = u1
    username_1    = models.ForeignKey(Users,db_column="username_1",related_name = 'from_user',to_field='username', on_delete=models.CASCADE)
    username_2    = models.ForeignKey(Users,to_field='username', related_name = 'to_user', db_column="username_2",on_delete=models.CASCADE)

    #Users.objects.filter(u_relate_u__username=<second_col>)    // <second_col> could be 'tan10'
    # >>> u1
    # <Users: rahul7>
    # >>> u1.u_relate_u.all()
    # <QuerySet [<Users: tan10>, <Users: akki>]>
    # for the other table in relationship we can do something like:
    # t2 = Table2.objects.get(some_parameter=value_u_want)
    # t2.users_set.all()    will give the objects of users related with t2
    def __str__(self):
        return  '{} blocks {}'.format(self.username_1, self.username_2)

    class Meta:
        db_table        = 'user_block_user'
        unique_together = (("username_1","username_2"))


class Notification(models.Model):
    #                   base_field        
    # likes       = ArrayField(models.BigIntegerField(null=True,blank=True),default=default_list)
    # dislikes    = ArrayField(models.BigIntegerField(null=True,blank=True),default=default_list)
    # reply       = ArrayField(models.BigIntegerField(null=True,blank=True), default=default_list)

    user_id         = models.ForeignKey(Users, db_column='user_id', blank=False, on_delete=models.CASCADE, related_name='my_notification')
    other_user_id   = models.ForeignKey(Users, db_column='other_user_id', blank=False, on_delete=models.CASCADE, related_name='sent_notification_to' )
    notification    = JSONField()

    def __str__(self):
        return '{} notify {}'.format(self.other_user_id,self.user_id)

    class Meta:
        db_table  = 'notifications'
        unique_together = (("user_id","other_user_id"))

