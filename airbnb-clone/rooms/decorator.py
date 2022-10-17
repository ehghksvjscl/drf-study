from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from django.shortcuts import get_object_or_404


def room_auth_check(func):
    def wrap(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        if request.user.is_authenticated:
            room = self.get_object(pk)

            # Permissionn
            if room.owner != request.user:
                raise PermissionDenied

            setattr(request, "room", room)

            return func(self, request, *args, **kwargs)

        else:
            raise NotAuthenticated

    return wrap
