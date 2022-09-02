"""View module for handling requests about gift preferences"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers 
from sleighmeapi.models.gift_preference import GiftPreference


class GiftPreferenceView(ViewSet):
    """Sleigh Me group preference views"""
    
    def list(self, request):
        """Handle GET reqeusts to get all gift preferences
        
        Returns:
            Response -- JSON serialized list of groups
        """
        
        gift_preference = GiftPreference.objects.all()
        serializer = GiftPreferenceSerializer(gift_preference, many=True)
        return Response(serializer.data)
    
class GiftPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftPreference
        fields = (
            'id',
            'option'
            )