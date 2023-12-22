from .models import ToDoItem,ToDoGroup
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoGroup
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        #fields = ['title','group','done','deadline_date']
        fields = '__all__'