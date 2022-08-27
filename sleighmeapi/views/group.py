"""View module for handling requests about groups"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from sleighmeapi.models.group import Group
from django.contrib.auth.models import User

class GroupView(ViewSet):
    """Sleigh Me group views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single group
        
        Returns:
            Response -- JSON serialized group
        """
        
        try:
            group = Group.objects.get(pk=pk)
            serializer = GroupSerializer(group)
            return Response(serializer.data)
        except Group.DoesNotExist as ex:
            return Response({'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all groups
        
        Returns:
            Response -- JSON serialized list of groups
        """
        
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    
 
class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'creator',
            'guidelines',
            'date',
            'time'
            )
        depth = 2
