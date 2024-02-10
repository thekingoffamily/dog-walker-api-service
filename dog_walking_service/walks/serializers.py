from rest_framework import serializers
from .models import WalkOrder

class WalkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkOrder
        fields = '__all__'