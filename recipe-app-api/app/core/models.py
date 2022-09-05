"""
Database models
"""

import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

def recipe_image_file_path(instance, filename):
    """image file path 생성"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)

# AbstractBaseUser를 사용하면 로그인 방식도 변경할 수 있고, 
# 원하는 필드들로 유저 모델을 구성할 수 있습니다. 
# 아래는 email, password를 활용하여 로그인하고 추가적으로 소속된 기관 정보만을 가지는 간단한 유저 모델을 구현하는 예시입니다. 
# 이 때 BaseUserManager를 상속하는 UserManager를 함께 정의하여 일반 유저 및 슈퍼유저의 생성 방식을 정의해줘야 합니다. 
# 또한 PermissionsMixin 을 함께 상속하면 Django의 기본그룹, 허가권 관리 등을 사용할 수 있습니다.

class UserManaager(BaseUserManager):
    """Manager for user"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """ Create Super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManaager()

    USERNAME_FIELD = "email"


class Recipe(models.Model):
    """Recipe object"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    """Tag for filtering recipe."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name