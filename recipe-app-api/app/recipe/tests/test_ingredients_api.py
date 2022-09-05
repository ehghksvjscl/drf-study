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
from recipe import serializers

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_user(email='user@example.com', password='testpassword'):
    """Create and reutnr a user"""
    return get_user_model().objects.create_user(email=email, password=password)

def detail_ingredient(ingredient_id):
    return reverse('recipe:ingredient-detail' ,args=[ingredient_id])

class PublicIngredientsAPITests(TestCase):
    """Test unauthenticated API request"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITests(TestCase):
    """Test  authenticated API request"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_list_ingredients(self):
        """Ingredients list call"""

        models.Ingredient.objects.create(user=self.user, name='Kale')
        models.Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = models.Ingredient.objects.all().order_by('-name')
        serializer = serializers.IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""
        new_user = create_user(email='user2@example.com')
        models.Ingredient.objects.create(user=new_user, name='Salf')
        ingredient = models.Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        ingredient = models.Ingredient.objects.create(user=self.user, name='Cilantro')

        payload = {
            'name': 'Coriander'
        }
        url = detail_ingredient(ingredient.id)
        res = self.client.patch(url, payload, foramt='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        ingredient = models.Ingredient.objects.create(user=self.user, name='Lettuce')
        
        url = detail_ingredient(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = models.Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """ Test listing ingredients by those assigned to recipe"""

        in1 = models.Ingredient.objects.create(user=self.user, name='Apples')
        in2 = models.Ingredient.objects.create(user=self.user, name='Turkey')
        recipe = models.Recipe.objects.create(
            title='Apple Crumble',
            time_minutes = 5,
            price=Decimal('4.40'),
            user=self.user
        )

        recipe.ingredients.add(in1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only':1})

        s1 = serializers.IngredientSerializer(in1)
        s2 = serializers.IngredientSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test filtered ingredients return a unique list"""

        ingrdient = models.Ingredient.objects.create(user=self.user, name='Eggs')
        models.Ingredient.objects.create(user=self.user, name='Lentils')
        recipe1 = models.Recipe.objects.create(
            title='Eggs Benedict',
            time_minutes = 40,
            price=Decimal('7.0'),
            user=self.user
        )
        recipe2 = models.Recipe.objects.create(
            title='Herb Eggs',
            time_minutes = 20,
            price=Decimal('4.0'),
            user=self.user
        )
        recipe1.ingredients.add(ingrdient)
        recipe2.ingredients.add(ingrdient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only':1})

        self.assertEqual(len(res.data), 1)