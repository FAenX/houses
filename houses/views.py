from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import *

from django.shortcuts import render
from .models import Manager, House, Tag, Manager, HouseInstance
from django.views import generic


def index(request):
    num_houses=House.objects.count()
    num_house_instances=HouseInstance.objects.count()
    num_house_instances_available=HouseInstance.objects.filter(availability=True).count()
    num_managers=Manager.objects.count()

    context = {
        'num_houses':num_houses,
        'num_house_instances':num_house_instances,
        'num_house_instances_available':num_house_instances_available,
        'num_managers':num_managers,
    }

    return render(request, 'index.html',context=context)

class HouseListView(generic.ListView):
    model = House
    paginate_by = 10

    def get_queryset(self):
        return House.objects.all()

class HouseDetailView(generic.DetailView):
    model = House


@api_view(['GET', 'POST'])
def manager_list(request):
    """
 List  Managers, or create a new Manager.
 """
    if request.method == 'GET':
        data = []
        nextPage = 1
        previousPage = 1
        managers = Manager.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(managers, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = ManagerSerializer(data,context={'request': request} ,many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previousPage = data.previous_page_number()

        return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/customers/?page=' + str(nextPage), 'prevlink': '/api/customers/?page=' + str(previousPage)})

    elif request.method == 'POST':
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def manager_detail(request, pk):
    """
    Retrieve, update or delete a Manager by id/pk.
    """
    try:
        manager = Manager.objects.get(pk=pk)
    except Manager.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ManagerSerializer(manager,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ManagerSerializer(manager, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
