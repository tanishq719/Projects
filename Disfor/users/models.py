from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from rest_framework_simplejwt.tokens import Token
from passlib.hash import pbkdf2_sha256
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import numpy as np

class UserManager(BaseUserManager):
    def create_user(self, username, first_name='Gully', last_name="Boy", join_date=None,
                    email=None, last_login=None, reputation=0, password=None,
                    like_count=0, dislike_count=0, reply_count=0,description='',dp = None):
        if not username:
            raise ValueError("Users must have an username")
        if not password:
            raise ValueError("Users must have an password")

        user_obj = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            join_date = join_date,
            email = self.normalize_email(email),
            last_login = last_login,
            reputation = reputation,
            like_count = like_count,
            dislike_count = dislike_count,
            reply_count = reply_count,
            description = description,
            dp = dp
        )
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, first_name='Gully', last_name="Boy", join_date=None,
                    email=None, last_login=None, reputation=0, password=None,
                    like_count=0, dislike_count=0, reply_count=0,description='',dp = None):
        return create_user(username,first_name,last_name,join_date,email,last_login,reputation, password,like_count,dislike_count,reply_count,description,dp)

class Users(AbstractBaseUser):

    username            = models.CharField(max_length = 25, primary_key = True)
    first_name          = models.CharField(max_length = 25, null=False, blank=False)
    last_name           = models.CharField(max_length = 25, null=False, blank=False)
    join_date           = models.DateField(auto_now_add=True) # doubtfull
    email               = models.EmailField(null=False, blank=False, unique=True, max_length=60)
    last_login          = models.DateTimeField(auto_now = True) # doubtful
    reputation          = models.IntegerField(default=0,blank=True)
    password            = models.CharField(max_length=256,null=False, blank=False)
    like_count          = models.IntegerField(default=0,blank=True)
    dislike_count       = models.IntegerField(default=0,blank=True)
    reply_count         = models.IntegerField(default=0,blank=True)
    # discription about user
    description         = models.CharField(max_length = 200, default = "null",null=False, blank=False)
    dp                  = models.ImageField(upload_to='profile_image', blank=False, default='user.png')

    u_relate_u          = models.ManyToManyField('self',through='User_block_user', blank=True, symmetrical=False)
    #u1.u_relate_u.add(u2)
    #u1.u_relate_u.create(atributes....)
    # user_block_user     = models.ManyToManyField('self',related_name='from_user',blank=True, symmetrical=False)
    #u1.user_block_user.add(u2)


    REQUIRED_FIELDS = ('first_name','last_name','email','password','description')
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
    
    def __unicode__(self):
        return '{0}'.format(self.dp)

    def save(self):
        if not self.dp:
            return

        image = Image.open(self.dp)
        size = ( 200, 200)
        image = image.resize(size, Image.ANTIALIAS)
        image_file = BytesIO()
        image.save(image_file,format='PNG')
        self.dp.save(self.dp.name, InMemoryUploadedFile(
            image_file,
            None, '',
            self.dp.file.content_type,
            image.size,
            self.dp.file.charset,
        ), save=False)
        super(Users, self).save()

    @staticmethod
    def get_hashed(password):
        return pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
        
    @staticmethod
    def verify_password(raw_password, hash_password):
        return pbkdf2_sha256.verify(raw_password, hash_password)

    @staticmethod
    def get_object(values:dict):
        return Users(
            username=values['username'], first_name=values['first_name'],
            last_name=values['last_name'], join_date=values['join_date'],
            email=values['email'],last_login=values['last_login'],
            reputation=values['reputation'],password=values['password'],
            like_count=values['like_count'],dislike_count=values['dislike_count'],
            reply_count=values['reply_count'],description=values['description'],
            dp=values['dp'])
        
    
#@@@@ USERS HISTORY TABLE @@@@

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
