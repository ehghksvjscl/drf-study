from rest_framework.exceptions import ParseError

from categories.models import Category


def get_category_or_400(category_pk):
    # Category
    if not category_pk:
        raise ParseError("Category is required")

    try:
        return Category.objects.get(
            pk=category_pk, kind=Category.CategoryKindChoices.ROOMSM
        )
    except Category.DoesNotExist:
        raise ParseError("Category not found")
