from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.headers.get("Trust-Me")
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            return AuthenticationFailed(f"User not found {username}")
