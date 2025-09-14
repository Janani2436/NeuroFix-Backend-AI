# users/serializers.py

from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# This serializer is still fine
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'role']

# Replace the existing RegisterSerializer with this one
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # We only need the fields the frontend will send
        fields = ('id', 'password', 'email', 'full_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # We create the user using our updated create_user method
        # The role will be set to the default ('STUDENT') automatically
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'] # Pass password here
        )
        # The set_password logic is now handled inside create_user,
        # but calling it again is safe and ensures it's hashed.
        # user.set_password(validated_data['password'])
        # user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['full_name'] = user.full_name
        token['role'] = user.role

        return token