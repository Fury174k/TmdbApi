from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Add username field

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'name', 'bio', 'profile_picture']  # Include username