from rest_framework import serializers
from .models import WalkOrder, Walker


class WalkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walker
        fields = ['id', 'name']

class WalkOrderSerializer(serializers.ModelSerializer):
    walker = WalkerSerializer(read_only=True)  # Добавляем сериализатор для выгульщика
    class Meta:
        model = WalkOrder
        fields = ['apartment_number', 'pet_name', 'pet_breed', 'walk_datetime', 'walker']
        # Теперь 'walker' включен в список полей