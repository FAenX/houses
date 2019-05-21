from django.db import models
from django.utils.timezone import now
import uuid
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_google_maps import fields as map_fields


User = get_user_model()

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name='tag'
        verbose_name_plural='tags'
        ordering=['name']

    def __str__(self):
        return self.name

class House(models.Model):

    name=models.CharField(max_length=250, help_text='Enter House Name')
    description=models.TextField('description',blank=True)
    date_created=models.DateTimeField('date created')
    date_updated=models.DateTimeField('date updated')
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag,blank=True)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name='house'
        verbose_name_plural='houses'
        ordering=['-date_created']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.id:
            self.date_created=now()
        self.date_updated=now()
        super(House,self).save(*args,**kwargs)

    def get_absolute_url(self):
        """return the url to access the detail record of this house"""
        return reverse('house-detail',args=[str(self.id)])

class HouseInstance(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID field')
    house=models.ForeignKey(House, on_delete=models.SET_NULL,null=True)
    availability=models.BooleanField(default=False)

    class Meta:
        ordering=['availability']

    def __str__(self):
        return f'{self.id} ({self.house.name})'


