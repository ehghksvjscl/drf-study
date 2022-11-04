from django.db import transaction

from rest_framework.exceptions import ParseError

from categories.crud import get_category_or_400


def create_experience_category(request, experience_serializer):
    """
    create experience with category

    parms: request , serializer, category
    """
    try:
        # Start transction
        with transaction.atomic():
            category_pk = request.data.get("category")
            category = get_category_or_400(category_pk, is_experience=True)

            # experience
            experience = experience_serializer.save(
                host=request.user, category=category
            )

    except Exception:
        raise ParseError("Category not found")

    return experience
