from rest_framework.exceptions import ParseError

from categories.models import Category


def get_category_or_400(category_pk, is_experience=False):
    """
    get category or raise 400 error

    Parms: category_pk, is_experience
        is_experience: True if experience is experience
    """
    if not category_pk:
        raise ParseError("Category is required")

    try:
        if is_experience:
            return Category.objects.get(
                pk=category_pk, kind=Category.CategoryKindChoices.EXPERIENCES
            )
        else:
            return Category.objects.get(
                pk=category_pk, kind=Category.CategoryKindChoices.ROOMSM
            )
    except Category.DoesNotExist:
        raise ParseError("Category not found")
