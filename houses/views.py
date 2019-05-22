#
import uuid
import json

#django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.core import serializers

#django google maps
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields


#houses
from .serializers import *
from .models import House, Tag, HouseInstance, Image
from .forms import CreateHouseForm

User = get_user_model()

class IndexView(TemplateView):
    '''
    houses index view
    '''

    template_name = 'houses/index.html'

    def get_context_data(self, *args, **kwargs):
        #add querysets to context
        
        context = super().get_context_data(*args, **kwargs)
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['images'] = Image.objects.all()
        context['houses'] = House.objects.all() 
        context['num_houses'] = House.objects.count()
        context['num_house_instances'] = HouseInstance.objects.count()
        context['num_house_instances_available'] = HouseInstance.objects.filter(availability=True).count()
        context['num_landlords'] = User.objects.filter(is_landlord=True).count()
        
        return context

class HouseListView(ListView):
    '''
    house list view
    '''
    model = House
    paginate_by = 10

    

class HouseDetailView(DetailView):
    '''
    gouse detail view
    '''
    class Meta:
        model = House 

    model = House
    template_name = 'houses/house_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = House.objects.get(slug=self.kwargs['slug'])
        context['images'] = Image.objects.filter(house=house)
        return context

class HouseCreateView(CreateView):
    '''
    house create view
    '''
    model = House
    template_name = 'houses/create_house.html'
    form_class = CreateHouseForm


     
