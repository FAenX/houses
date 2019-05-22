from django.db import models
from django.utils.timezone import now
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_google_maps import fields as map_fields
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


User = get_user_model()


class Tag(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text='Unique ID field')
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    '''
    House category
    '''
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text='Unique ID field')
    name = models.CharField(_('Category'), max_length=40)

class Image(models.Model):
    '''
    images model
    '''
    title = models.CharField(_('Image title'), max_length=10)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True)
    house = models.ForeignKey('House', on_delete=models.SET_NULL, null=True)


class House(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text='Unique ID field')
    name = models.CharField(max_length=250, help_text='Enter House Name')
    description = models.TextField('description', blank=True)
    date_created = models.DateTimeField(_('Creattion date'), auto_now=True)
    date_updated = models.DateTimeField('date updated')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ManyToManyField(Category)
    

    class Meta:
        verbose_name = 'house'
        verbose_name_plural = 'houses'
        ordering = ['-date_created']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(House, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """return the url to access the detail record of this house"""
        return reverse('house-detail', args=[str(self.slug)])


class HouseInstance(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text='Unique ID field')
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True)
    availability = models.BooleanField(default=False)
    room_number = models.CharField(_('Room/House Number'), max_length=20)

    class Meta:
        ordering = ['availability']

    def __str__(self):
        return f'{self.house.name} {self.room_number}'

# pre_save conditions
# create slugs for models with slug field

############################
@receiver(pre_save, sender=House)
def create_house_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user)

@receiver(pre_save, sender=Image)
def create_house_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

