from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import ToDoGroup, ToDoItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from todo.serializers import GroupSerializer, ItemSerializer
from django.contrib.auth import logout


# Create your views here.


def home_view(request):
   if request.user.is_authenticated:
       user = request.user
       groups = request.user.todogroup_set.all()
       if request.method == 'POST':
           if request.POST.get('submit'):
               title = request.POST.get('title')
               request.user.todogroup_set.create(group_title=title)

       return render(request, 'todo/home.html', {'groups': groups})
   return render(request, 'todo/home.html')


def group_view(request, id):
    group = ToDoGroup.objects.get(id=id)
    items = group.item.all()
    if request.method == 'POST':
        if request.POST.get('save'):
            for item in items:
                if request.POST.get(f't{item.id}')=='on':
                    item.done = True
                else:
                    item.done = False
                item.save()
        elif request.POST.get('create'):
            new_item = ToDoItem.objects.create(title=request.POST.get('text'), group = group)
            new_item.save()
    items = group.item.all().order_by('-done')
    return render(request, 'todo/group.html', {'group': group, 'items': items})

@api_view(['GET','POST'])
def group_list(request, format=None):#gets the json of existing groups or creates a group
    if request.method == 'GET':
        group = ToDoGroup.objects.all()
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def group_detail(request, pk, format=None):# retrieve delete update
    try:
        group = ToDoGroup.objects.get(pk=pk)
    except ToDoGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def item_view_api(request, id):
    group = ToDoGroup.objects.get(id=id)
    item = group.item.all()
    serializer = ItemSerializer(item, many=True)
    return Response(serializer.data)

