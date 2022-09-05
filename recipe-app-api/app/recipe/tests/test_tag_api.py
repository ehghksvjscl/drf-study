"""
Tests for the tags API.
"""

from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')

def detail_url(tag_id):
    """Create and return a tag detail url"""
    return reverse('recipe:tag-detail', args=[tag_id])

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

    def test_update_tag(self):
        """Tage updating a tag"""

        tag = models.Tag.objects.create(user=self.user, name='After')
        payload = {
            'name':'Dessert'
        }
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag"""

        tag = models.Tag.objects.create(user=self.user, name='Breakfrst')
        
        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Tag.objects.filter(user=self.user).exists())

    def test_filter_tags_assigned_to_recipes(self):
        """Test listing tags to those assogned tp recipes."""

        tag1 = models.Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = models.Tag.objects.create(user=self.user, name='Lunch')
        recipe = models.Recipe.objects.create(
            title='Green Eggs on Toast',
            time_minutes = 10,
            price=Decimal('2.50'),
            user=self.user
        )

        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only':1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags return a unique list"""

        tag = models.Tag.objects.create(user=self.user, name='Brealfast')
        models.Tag.objects.create(user=self.user, name='Dinner')
        recipe1 = models.Recipe.objects.create(
            title='Pancakes',
            time_minutes = 5,
            price=Decimal('5.0'),
            user=self.user
        )
        recipe2 = models.Recipe.objects.create(
            title='Porridge',
            time_minutes = 3,
            price=Decimal('2.0'),
            user=self.user
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only':1})

        self.assertEqual(len(res.data), 1)