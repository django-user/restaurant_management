"""restaurant app admin"""
from django.contrib import admin

from .models import RestaurantMenu, RestaurantMenuVote, WinningRestaurant

admin.site.register(RestaurantMenuVote)
admin.site.register(RestaurantMenu)

@admin.register(WinningRestaurant)
class WinningRestaurantAdmin(admin.ModelAdmin):
    """Admin class for WinningRestaurant model"""
    list_display = ('restaurant', 'created_at',)
