from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from houses.models import House, HouseInstance, Tag, Category, Image


class HouseInstanceInline(admin.TabularInline):
    model = HouseInstance


@admin.register(House)
class HouseAdmin(OSMGeoAdmin):
    formfield_overrides = {
        map_fields.AddressField: {
            'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
    }

    list_display = ['name', 'date_created', 'geom', 'landlord', 'get_categories']
    inlines = [HouseInstanceInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(HouseInstance)
class HouseInstanceAdmin(admin.ModelAdmin):
    list_filter = ['availability']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
    category admin
    '''

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    '''
    category admin
    '''
