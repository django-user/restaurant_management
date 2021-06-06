"""Restaurant app views"""
import logging
from datetime import date, datetime

from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from accounts.models import User
from .serializers import RestaurantMenuSerializer, RestaurantSerializer
from .models import RestaurantMenu, RestaurantMenuVote, WinningRestaurant


logging.basicConfig(level = logging.ERROR, filename = 'restaurant.log')


class RestaurantMenuViewSet(viewsets.ModelViewSet):
    """ViewSet class to get, edit RestaurantMenu objects"""
    serializer_class = RestaurantMenuSerializer

    def get_queryset(self):
        return RestaurantMenu.objects.filter(restaurant=self.request.user)

    def perform_create(self, serializer):
        serializer.save(restaurant=self.request.user)

    def perform_update(self, serializer):
        serializer.save(restaurant=self.request.user)


class RestaurantMenuAPIView(APIView):
    """A class based view for fetching restaurant menus"""
    def get(self, request):
        """
        Get all the restaurants and today's menus records
        :return: Returns a list of restaurant's menus
        """
        #Check if any restaurant is winner for 2 consecutive days, as it can't be on 3rd day
        restaurants = User.objects.filter(is_restaurant=True)
        won_restaurant = WinningRestaurant.objects.select_related('restaurant')\
            .order_by('created_at')
        id_set = won_restaurant[:2].values_list('restaurant__id', flat=True)
        if len(set(id_set)) == 1:
            restaurants = restaurants.exclude(id=id_set[0])
        #get restaurant and menu data available for today
        serializer = RestaurantSerializer(instance=restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a vote for menu in the database"""
        if request.user.is_employee:
            try:
                menu = RestaurantMenu.objects.get(id=request.data.get("menu_id"),
                                           date=date.today())
                vote = RestaurantMenuVote.objects.get(
                    vote_by=request.user, created_at=datetime.now())
                vote.menu = menu
                vote.save()
            except RestaurantMenu.DoesNotExist:
                raise Http404("Menu details missing")
            except RestaurantMenuVote.DoesNotExist:
                RestaurantMenuVote.objects.create(vote_by=request.user, menu=menu)
            return Response({"message": "Vote submitted successfully."})
        else:
            return Response({"message": "You are not authorise to submit a vote."})

class GetWinnerRestaurantView(ListAPIView):
    def get(self, request):
        try:
            restaurant = WinningRestaurant.objects.get(created_at=date.today()).restaurant
            serializer = RestaurantSerializer(instance=restaurant)
            return Response(serializer.data)
        except Exception as e:
            logging.error("An Error Logging while updating winning restaurant")
            return Response({"message": "You are not authorise to submit a vote."})
