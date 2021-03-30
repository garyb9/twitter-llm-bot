from rest_framework import serializers

from .models import TokenURI


class TokenURISerializer(serializers.ModelSerializer):
    """Serializer for TokenURI object"""
    id      = serializers.UUIDField(format='hex', read_only=True)

    class Meta:
        model = TokenURI
        fields = (
            'id', 'address',
        )
        read_only_Fields = ('id',)
        extra_kwargs = {
            'id':{'read_only':True,},
        }
    
    def create(self, validated_data):
        """Create a new TokenURI and return it"""
        return TokenURI.objects.create_TokenURI(**validated_data)