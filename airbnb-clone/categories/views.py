from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_object_or_404

from categories.models import Category
from categories.serializers import CategorySerializer


class CategoriesView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
