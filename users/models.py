from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime

from django.utils.text import slugify





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
    is_landlord = models.BooleanField('I am Looking for Work', default=False)
    is_tenant = models.BooleanField('I am Hiring', default=False)
    slug = models.SlugField(unique=True)
                

    username = None

    objects = UserManager()
    #use email as username fields
    USERNAME_FIELD = 'email'
    #over right REQUIRED_FIELDS to empty
    REQUIRED_FIELDS = []

class LandlordProfile(models.Model):
    '''
    landlord profile model
    '''
    user = models.OneToOneField(User, related_name='landlordprofile', on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField('Created At',auto_now_add=True)
    slug  = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.user.first_name},{self.user.last_name}'

###########################

#pre_save conditions
#create slugs for models with slug field

############################
@receiver(pre_save, sender=LandlordProfile)
def create_Landlordprofile_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user)
        


@receiver(pre_save, sender=User)
def create_user_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.first_name, instance.last_name)
        

###############

#post_save user profile

##############
@receiver(post_save, sender=User)
def create_Profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_landlord:
            LandlordProfile.objects.create(user=instance)
        else:
            pass
            

