"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

class UserView(ViewSet):
    """SleighMe users views"""
    
    def retrieve(self, request, pk):
        """Handle Get requests to get a single user
        
        Returns:
            Response -- JSON serialized post
        """
        
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return (Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND))
        
    def list(self, request):
        """Handle Get requests to get all users
        
        Returns:
            Response -- JSON serialized list of users
        """
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )
        depth = 2