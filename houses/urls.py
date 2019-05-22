
from django.urls import path
from . import views


urlpatterns=[
    
    path('house-list/',views.HouseListView.as_view(),name='houses_list'),
    path('house/<slug:slug>/', views.HouseDetailView.as_view(), name='house_detail'),
    path('create-entry/', views.HouseCreateView.as_view(), name='create_house'),
] 

