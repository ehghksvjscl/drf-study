from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from django.shortcuts import get_object_or_404


def room_owner_check(func):
    def wrap(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        room = self.get_object(pk)

        # Permissionn
        if room.owner != request.user:
            raise PermissionDenied

        setattr(request, "room", room)

        return func(self, request, *args, **kwargs)

    return wrap
