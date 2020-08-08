from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
# todoList: id, name, priority
# listItem: id, title, description, due_date, iscompleted


from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class TodoList(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, null=False, unique=True)
    priority = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)
    owner = models.ForeignKey(
        MyUser, related_name="has_todolist", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} list'.format(self.title)

    class Meta:
        db_table = 'todolist'


class TodoItem(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)
    due_date = models.DateField(null=False)
    isCompleted = models.BooleanField(default=False)

    parent_list = models.ForeignKey(TodoList, db_column='parent_list', related_name='items', on_delete=models.CASCADE,null=True)

    def save(self, *args, **kwargs):
        print("something")
        super(TodoItem,self).save(*args,**kwargs)

    class Meta:
        db_table = 'todoitem'

    def __str__(self):
        return '{} item'.format(self.title)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
