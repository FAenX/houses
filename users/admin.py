from django.contrib import admin
from .models import LandlordProfile, User

@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    '''
    landlord profile admin
    '''

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    '''
   User admin
    '''
    
