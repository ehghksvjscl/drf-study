"""
Django admin 커스터마이징
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    """User Admin Define"""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        ('CostomUser', {'fields': ('email', 'password')}),
        (
            _('Permisssions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important datas'), {'fields': ['last_login']}
        )
    )
    readonly_fields = ['last_login']
admin.site.register(models.User, UserAdmin)
