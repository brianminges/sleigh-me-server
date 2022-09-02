"""View module for handling requests about profiles"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from django.contrib.auth.models import User
from sleighmeapi.models.gift_preference import GiftPreference
from sleighmeapi.models.state import State
from sleighmeapi.models.profile import Profile

class ProfileView(ViewSet):
    """Sleigh Me profile views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single profile
        
        Returns:
            Response -- JSON serialized profile
        """
        
        try:
            profile = Profile.objects.get(pk=pk)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist as ex:
            return Response({'message': ex.arg[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk):
        """Handle PUT operations
        
        Returns
            Response -- JSON serialized profile instance
        """
        profile = Profile.objects.get(pk=pk)
        gift_preference = GiftPreference.objects.get(pk=request.data["gift_preference"])
        state = State.objects.get(pk=request.data["state"])
        
        profile.likes = request.data["likes"]
        profile.dislikes = request.data["dislikes"]
        profile.gift_preference = gift_preference
        profile.street = request.data["street"]
        profile.city = request.data["city"]
        profile.state = state
        profile.zip = request.data["zip"]
        profile.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
       
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'id',
            'likes',
            'dislikes',
            'gift_preference',
            'street',
            'city',
            'state',
            'zip',
            'member'
        )
        depth = 2