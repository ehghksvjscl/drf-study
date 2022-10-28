from django.contrib.auth import login, authenticate, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import PrivateUserSerializer
from users.models import User


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        serializer = PrivateUserSerializer(data=request.data)
        password = request.data.get("password")
        if not password:
            raise ParseError

        if serializer.is_valid():
            user = serializer.save()

            user.set_password(password)
            user.save()

            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get_user(self, username):
        return get_object_or_404(User, username=username)

    def get(self, request, username):
        user = self.get_user(username)
        return Response(PrivateUserSerializer(user).data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


""" {
"username":"admin","password":"admin"
}
"""
class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise ParseError

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message":"200"})
        else:
            return Response({"error":"Wrong password"})

class LogOut(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"message":"200"})
