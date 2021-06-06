"""test cases for restaurants app"""
from django.urls import reverse

from rest_framework.test import APITestCase

from accounts.models import User
from .models import RestaurantMenu

class RestaurantMenuTests(APITestCase):
    """RestaurantMenuViewSet Unit Test cases"""
    def setUp(self):
        self.employee_user = User.objects.\
            create(username="employee", password="password", is_employee=True)
        self.restaurant_user = User.objects\
            .create(username="restaurant", password="password",
                    is_restaurant=True, is_employee=False)
        self.menu = RestaurantMenu.objects.create(name="Burger",
                                                  restaurant=self.restaurant_user)
        # self.client.force_authenticate(self.employee_user)
        # self.assertTrue(self.client.login(username='employee', password='password'))

    def test_get_menu_list(self):
        """
        Ensure we can get a menu list.
        """
        url = reverse('restaurant-menu-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.restaurant_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_menu(self):
        """
        Ensure we can get a menu list.
        """
        url = reverse('restaurant-menu-list')
        response = self.client.post(url, {'name': 'Burger'})
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.restaurant_user)
        response = self.client.post(url, {'name': 'Burger'})
        self.assertEqual(response.status_code, 201)

    def test_get_menu(self):
        """
        Ensure we can get a menu list.
        """
        url = reverse('restaurant-menu-detail', args=[self.menu.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.restaurant_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)


class RestaurantsTests(APITestCase):
    """
    RestaurantMenuAPIView Unit Test cases, get restaurant-wise menu and post a vote
    """
    def setUp(self):
        self.employee_user = User.objects.\
            create(username="employee", password="password", is_employee=True)
        self.restaurant_user = User.objects\
            .create(username="restaurant", password="password",
                    is_restaurant=True, is_employee=False)
        self.menu = RestaurantMenu.objects.create(name="Burger",
                                                  restaurant=self.restaurant_user)

    def test_get_menu_list(self):
        """
        Ensure we can get a menu list.
        """
        url = reverse('restaurants')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.employee_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_vote(self):
        """
        Ensure we can get a menu list.
        """
        url = reverse('restaurants')
        response = self.client.post(url, {'menu_id': self.menu.id})
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.employee_user)
        response = self.client.post(url, {'menu_id': self.menu.id})
        self.assertEqual(response.status_code, 200)
