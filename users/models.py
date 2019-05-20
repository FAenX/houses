from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime





# Create your models here.

class UserManager(BaseUserManager):
    '''
    user manager
    '''
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given employee_id email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    '''
    user model
    '''

    email = models.EmailField(_('Email Address'), blank=False, unique=True)
    first_name = models.CharField(_('First Name'), max_length=50, blank=False)
    last_name = models.CharField(_('Last Name'), max_length=50, blank=False)
    is_manager = models.BooleanField('I am Looking for Work', default=False)
    is_tenant = models.BooleanField('I am Hiring', default=False)
    slug = models.SlugField(unique=True)
                

    username = None

    objects = UserManager()
    #use email as username fields
    USERNAME_FIELD = 'email'
    #over right REQUIRED_FIELDS to empty
    REQUIRED_FIELDS = []
