"""View module for handling requests about groups"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from sleighmeapi.models.group import Group
from sleighmeapi.models.member import Member
from sleighmeapi.models.partner import Partner
from django.contrib.auth.models import User
from sleighmeapi.views.partner import PartnerSerializer


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
        # Makes creator of group a member of it upon creation
        group.members.add(creator)
        serializer = CreateGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a group
        
        Returns:
            Response -- Empty body with 204 status code
        """
        
        group = Group.objects.get(pk=pk)
        creator = Member.objects.get(pk=request.data["creator"])
        group.name = request.data["name"]
        group.creator = creator
        group.guidelines = request.data["guidelines"]
        group.date = request.data["date"]
        group.time = request.data["time"]
        group.spend = request.data["spend"]
        group.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        """Handle DELETE requests for a group"""
        group = Group.objects.get(pk=pk)
        group.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['post'], detail=True)
    def join_group(self, request, pk):
        """Post request to add a member to a group"""
        group = Group.objects.get(pk=pk)
        member = request.data['member']
        group.members.add(member) 
        return Response({'message': 'User added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request of a user to leave a group"""
        member = Member.objects.get(user=request.auth.user)
        group = Group.objects.get(pk=pk)
        group.members.remove(member)
        return Response({'message': 'User removed'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True)
    def partner_alert(self, request, pk):
        """ Gets user's partner pairing """
        try: 
            group = Group.objects.get(pk=pk)
            giver = Member.objects.get(user=request.auth.user)
            partner = Partner.objects.get(giver_id=giver.id, group_id=group.id)
            serializer = PartnerSerializer(partner)
            return Response(serializer.data)
        except Partner.DoesNotExist as ex:
            return Response({'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND)
  
    

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
            'members',
            'partners'
        )
        depth = 3


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