"""Account app serializers"""
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from allauth.utils import (email_address_exists, get_username_max_length)

from .models import User

class RegisterSerializer(serializers.Serializer):
    """RegisterSerializer serializer class for registration API"""
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=allauth_settings.USERNAME_REQUIRED
    )
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    is_restaurant = serializers.BooleanField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        """RegisterSerializer method to validate username"""
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        """RegisterSerializer method to validate an email"""
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        """RegisterSerializer method to validate password"""
        return get_adapter().clean_password(password)

    def validate(self, data):
        """RegisterSerializer method to validate both password"""
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        """RegisterSerializer method to get cleaned data"""
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'is_restaurant': self.validated_data.get('is_restaurant', ''),
        }

    def save(self, request):
        """RegisterSerializer method to save registration form data"""
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        user.is_restaurant = self.cleaned_data.get('is_restaurant', False)
        if self.cleaned_data.get('is_restaurant'):
            user.is_employee = False
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

class UserDetailsSerializer(serializers.ModelSerializer):
    """A serializer class to get custom user details"""
    class Meta:
        """UserDetailsSerializer meta class"""
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_restaurant', 'is_employee')
        read_only_fields = ('username', 'is_restaurant', 'is_employee')
