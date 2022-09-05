"""View module for handling requests about members"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from sleighmeapi.models import Member
from sleighmeapi.models import Group
from django.contrib.auth.models import User
from django.db.models import Q

class MemberView(ViewSet):
    """Sleigh Me members views"""
    
    def retrieve(self, request, pk):
        """Handle Get requests to get a single member
        
        Returns:
            Response -- JSON serialized post
        """
        
        try:
            member = Member.objects.get(pk=pk)
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist as ex:
            return (Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND))
        
    def list(self, request):
        """Handle Get requests to get all members
        
        Returns:
            Response -- JSON serialized list of members
        """
        
        members = Member.objects.all()
        # Searches member names based on user's query
        search_name = self.request.query_params.get('q', None)
        if search_name is not None:
            members = User.objects.filter(
                Q(last_name__contains=search_name) |
                Q(first_name__contains=search_name)
            )
            serializer = MemberSearchSerializer(members, many=True)
            return Response(serializer.data)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
           
 
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'user',
            'profile',
            'groups'
            )
        depth = 6
        
class MemberSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'member'
        )
        depth = 2