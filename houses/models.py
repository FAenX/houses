from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils.timezone import now
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
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

    def __str__(self):
        return self.name

class Image(models.Model):
    '''
    images model
    '''
    title = models.CharField(_('Image title'), max_length=10)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(unique=True)
    house = models.ForeignKey('House', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class House(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, help_text='Unique ID field')
    name = models.CharField(max_length=250, help_text='Enter House Name')
    description = models.TextField('description', blank=True)
    date_created = models.DateTimeField(_('Creattion date'), auto_now=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    slug = models.SlugField(blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    geom = geomodels.PointField()
    

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

    def get_categories(self):
        return self.categories.all()

    def get_absolute_url(self):
        """return the url to access the detail record of this house"""
        return reverse('house_detail', kwargs={'slug': self.slug})


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

