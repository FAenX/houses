from django import forms
from django_google_maps.widgets import GoogleMapsAddressWidget
from .models import House


class CreateHouseForm(forms.ModelForm):
    '''
    create house form
    '''
    class Meta:
        model = House
        fields = '__all__'

    def form_valid(self, form):
        house = form.save()
        return house
        

