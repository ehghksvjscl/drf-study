from strawberry.permission import BasePermission
from typing import Any


class OnlyLoggedIn(BasePermission):
    message = "You must be logged in to access this data."

    def has_permission(self, source: Any, info):
        return info.context.request.user.is_authenticated
