

from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import FreelancerSignUpSerializer, ClientSignUpSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # Import IsAuthenticated directly
from .permissions import IsClientUser, IsFreelancerUser

class FreelancerSignUpView(generics.GenericAPIView):
    serializer_class = FreelancerSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()  # This returns the user object

        user_serialized = UserSerializer(user_data['user'])  # Use the user from the return value
        return Response({
            "user": user_serialized.data,
            "token": user_data['token'],  # Use the token returned from serializer
            "message": "Account created successfully",
        })

class ClientSignUpView(generics.GenericAPIView):
    serializer_class = ClientSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()  # This returns the user object

        user_serialized = UserSerializer(user_data['user'])  # Use the user from the return value
        return Response({
            "user": user_serialized.data,
            "token": user_data['token'],  # Use the token returned from serializer
            "message": "Account created successfully",
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_client': user.is_client
        })

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsClientUser]  # Use a list to combine permissions
    serializer_class = UserSerializer 

    def get_object(self):
        return self.request.user

class FreelancerOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsFreelancerUser]  # Use a list to combine permissions
    serializer_class = UserSerializer 

    def get_object(self):
        return self.request.user
