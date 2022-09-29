from rest_framework.decorators import api_view
from rest_framework.response import Response

from categories.models import Category
from categories.serializers import CategorySerializer


@api_view()
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    payload = {
        "200": "ok",
        "categories": serializer.data
    }

    return Response(payload)
