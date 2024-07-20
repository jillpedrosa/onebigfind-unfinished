from rest_framework import serializers
from .models import LostItem, FoundItem

class LostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostItem
        fields = ['id', 'name', 'description', 'brand', 'color', 'size', 'unique_features', 'date_lost', 'location_lost', 'photo', 'user', 'is_matched']

class FoundItemSerializer(serializers.ModelSerializer):
    lost_item = LostItemSerializer(read_only=True)  # Optionally include lost item details

    class Meta:
        model = FoundItem
        fields = ['id', 'name', 'description', 'brand', 'color', 'size', 'unique_features', 'date_found', 'location_found', 'photo', 'user', 'lost_item', 'is_notified']