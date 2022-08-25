"""
Tests for the tags API.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def create_user(email='user@example.com', password='testpassword'):
    """Create and reutnr a user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagAPITests(TestCase):
    """Test unauthenticated API request"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITests(TestCase):
    """Test  authenticated API request"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_list_tags(self):
        """Tags list call"""

        models.Tag.objects.create(user=self.user, name='Vegen')
        models.Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = models.Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        new_user = create_user(email='user2@example.com')
        models.Tag.objects.create(user=new_user, name='Fruity')
        tag = models.Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
