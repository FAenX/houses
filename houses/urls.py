from django.urls import path
from . import views

urlpatterns=[
    
    path('house-list/',views.HouseListView.as_view(),name='house-list'),
    path('house/<int:pk>', views.HouseDetailView.as_view(), name='house-detail'),
]
