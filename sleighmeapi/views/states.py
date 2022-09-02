"""View module for handling requests about states"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers 
from sleighmeapi.models.state import State
 
class StateView(ViewSet):
    """Sleigh Me state views"""
    
    def list(self, request):
        """Handle GET requests o get all states
        
        Returns:
            Response -- JSON serialized list of states
        """
        
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)
    
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = (
            'id',
            'name',
            'abbreviation'
            )