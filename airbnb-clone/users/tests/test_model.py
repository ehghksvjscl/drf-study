from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email="test@example.com", password="testpassword123"):
    """Create user funtion"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """유저를 생성한다."""

        email = "test@example.com"
        password = "testpassword"
        user = create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
