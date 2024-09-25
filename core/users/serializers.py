from rest_framework import serializers
from .models import Client, User, Freelancer
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_client']

class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

class ClientSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        user.set_password(password)
        user.is_client = True
        user.save()

        Client.objects.create(user=user)

        # Check if a token already exists for this user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the user and the token key
        return {
            'user': user,  # Return the user object
            'token': token.key  # Return the token (whether newly created or existing)
        }

class FreelancerSignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        user.set_password(password)
        user.is_freelancer = True
        user.save()

        # Check if a token already exists for this user
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the user and the token key
        return {
            'user': user,  # Return the user object
            'token': token.key  # Return the token (whether newly created or existing)
        }
