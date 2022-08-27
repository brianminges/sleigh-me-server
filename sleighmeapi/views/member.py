"""View module for handling requests about members"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from sleighmeapi.models import Member

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
        