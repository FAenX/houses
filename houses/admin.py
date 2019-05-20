from django.contrib import admin
from houses.models import House, HouseInstance, Manager, Tag

class HouseInstanceInline(admin.TabularInline):
    model=HouseInstance

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display=['name','date_created']
    inlines=[HouseInstanceInline]

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['name']

@admin.register(HouseInstance)
class HouseInstanceAdmin(admin.ModelAdmin):
    list_filter=['availability']
