"""View module for handling requests about groups"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from sleighmeapi.models.group import Group
from sleighmeapi.models.member import Member
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
    
    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized game instance
        """
        creator = Member.objects.get(user=request.auth.user)
        group = Group.objects.create(
            creator = creator,
            name = request.data["name"],
            guidelines = request.data["guidelines"],
            date = request.data["date"],
            time = request.data["time"],
            spend = request.data["spend"]
        )
        serializer = CreateGroupSerializer(group)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
 
class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'creator',
            'guidelines',
            'date',
            'time',
            'spend',
            'members'
            )
        depth = 2


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'creator',
            'guidelines',
            'date',
            'time',
            'spend'
        )