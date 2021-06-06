"""accounts app admin"""
from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """UserAdmin class to display list of users in admin panel"""
    list_display = ('username', 'is_restaurant', 'is_employee')
    list_filter = ('is_employee','is_restaurant')
