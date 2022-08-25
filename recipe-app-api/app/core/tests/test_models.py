"""
Tests for models.
"""

from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='testpassword123'):
    """Create user funtion"""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@example.com"
        password = 'testpassword'
        user = create_user(email,password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expect in sample_emails:
            user = create_user(email, 'sample123')
            self.assertEqual(user.email, expect)

    def test_new_user_without_email_raiises_error(self):
        """Test 유저를 생성할때 에러"""

        with self.assertRaises(ValueError):
            create_user('', 'test123')

    def test_create_superuser(self):
        """Test 슈퍼유저 생성"""
        
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test create recipe   """

        user = create_user("test@example","testpassword123")
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price= Decimal('5.50'),
            description='Sample recipe description'
        )

        self.assertEqual(str(recipe), recipe.title)
        
    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)