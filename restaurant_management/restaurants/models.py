"""restaurant app models"""
from django.db import models

from accounts.models import User


class RestaurantMenu(models.Model):
    """Model class for Restaurant Menu"""
    name = models.CharField(max_length=48)
    restaurant = models.ForeignKey(User, related_name="restaurant_menu",
                                   on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return "{} ({})".format(self.name, self.restaurant.username)


class RestaurantMenuVote(models.Model):
    """RestaurantMenuVote model class for menu votes"""
    menu = models.ForeignKey(RestaurantMenu, related_name="restaurant_menu",
                                   on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, related_name="vote",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class WinningRestaurant(models.Model):
    """WinningRestaurant model class"""
    restaurant = models.ForeignKey(User, related_name="restaurant",
                                   on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.restaurant.username
