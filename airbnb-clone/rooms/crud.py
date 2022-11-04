from rest_framework.exceptions import ParseError

from django.db import transaction

from rooms.models import Amenity


def create_room_amenites_or_category(request, room_serializer, category):
    """
    parms: request , serializer, category
    """
    try:
        # Start transction
        with transaction.atomic():

            # Room
            room = room_serializer.save(owner=request.user, category=category)
            room.amenities.clear()

            # Amenities
            amenities = request.data.get("amenities")
            for amenity_pk in amenities:
                amenity = Amenity.objects.get(pk=amenity_pk)
                room.amenities.add(amenity)

    except Exception:
        raise ParseError("Amenity not found")

    return room
