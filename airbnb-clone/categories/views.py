from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from categories.models import Category
from categories.serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        payload = {"200": "ok", "categories": serializer.data}
        return Response(payload)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):
    if request.method == "GET":
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "PUT":
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            update_categroy = serializer.save()
            return Response(CategorySerializer(update_categroy).data)
        else:
            return Response(serializer.errors)
    elif request.method == "DELETE":
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status.HTTP_204_NO_CONTENT)
