"""Restaurant app serializers"""
from datetime import date

from rest_framework import serializers

from accounts.models import User
from .models import RestaurantMenu

class FilteredListSerializer(serializers.ListSerializer):
    """Serializer class to filter today's menu list"""
    def to_representation(self, data):
        data = data.filter(date=date.today())
        return super(FilteredListSerializer, self).to_representation(data)

class RestaurantMenuSerializer(serializers.ModelSerializer):
    """RestaurantMenu model serializer class"""
    class Meta:
        """meta class RestaurantMenuSerializer"""
        list_serializer_class = FilteredListSerializer
        model = RestaurantMenu
        fields = ("id", "name",'date')
        read_only_fields = ("id", 'date')


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer class to get restaurant and menu details"""
    restaurant_menu = RestaurantMenuSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'restaurant_menu']
