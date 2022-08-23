"""
View for the user
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from user.serialisers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer