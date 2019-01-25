from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid
from django.urls import reverse

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name='tag'
        verbose_name_plural='tags'
        ordering=['name']

    def __str__(self):
        return self.name

class Manager(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    address=models.TextField(blank=True, null=True)
    description=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField('Created At',auto_now_add=True)

    class Meta:
        ordering = ['first_name','last_name']

    def __str__(self):
        return f'{self.last_name},{self.last_name}'

class House(models.Model):

    name=models.CharField(max_length=250, help_text='Enter House Name')
    description=models.TextField('description',blank=True)
    date_created=models.DateTimeField('date created')
    date_updated=models.DateTimeField('date updated')
    manager=models.ForeignKey(Manager, verbose_name='owner',
                            on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag,blank=True)

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


