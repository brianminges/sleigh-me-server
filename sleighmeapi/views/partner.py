"""View module for handling requests about partners"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from sleighmeapi.models.partner import Partner
from sleighmeapi.models.member import Member
from sleighmeapi.models.group import Group
from django.contrib.auth.models import User

class PartnerView(ViewSet):
    """Sleigh Me partner views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single partner pairing
        
        Returns:
            Response -- JSON serialized group
        """
        
        try: 
            partner = Partner.objects.get(pk=pk)
            serializer = PartnerSerializer(partner)
            return Response(serializer.data)
        except Partner.DoesNotExist as ex:
            return Response({'message': ex.art[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all partner pairings
        
        Returns:
            Response -- JSON serialized list of partners
        """
        
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns:
            Response -- JSON serialized partner instance
        """
        partner = Partner.objects.create(
            group = Group.objects.get(id=request.data["group"]),
            giver = Member.objects.get(user=request.data["giver"]),
            receiver = Member.objects.get(user=request.data["receiver"])
        )
        serializer = CreatePartnerSerializer(partner)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = (
            'id',
            'giver',
            'receiver',
            'group'
        )
        depth = 1
        
class CreatePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = (
            'id',
            'giver',
            'receiver',
            'group'
        )
        depth = 2
        