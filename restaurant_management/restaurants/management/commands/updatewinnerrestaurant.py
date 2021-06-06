"""Restaurant app command to get winning restaurant"""
import logging
from datetime import date

from django.db.models import Count, Max, F
from django.core.management.base import BaseCommand, CommandError

from restaurants.models import RestaurantMenuVote, WinningRestaurant,\
    RestaurantMenu

logging.basicConfig(level = logging.ERROR, filename = 'command.log')

class Command(BaseCommand):
    """management command to update winning restaurant in the database"""
    help = 'Updates the winning restaurant in the database'

    def handle(self, *args, **options):
        try:
            query_result = RestaurantMenuVote.objects.filter(created_at=date.today()).values(
                'menu').order_by().annotate(votes=Count('menu'))
            if query_result:
                maxval = max(query_result, key=lambda x: x['votes'])
                menu = RestaurantMenu.objects.get(id=maxval.get('menu'))
                winner = WinningRestaurant.objects.create(restaurant=
                                                          menu.restaurant)
                self.stdout.write(self.style.SUCCESS(
                    "Today's winner restaurant is {}".format(winner)))
        except Exception as e:
            logging.error("An Error {} while updating winning restaurant".
                          format(e))
