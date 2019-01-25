from rest_framework import serializers
from .models import Manager

class ManagerSerializer(serializers.ModelSerializer):

    class Meta:
        model=Manager
        fields=('pk','first_name','last_name','email','phone','address','description')


