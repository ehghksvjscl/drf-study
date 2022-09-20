from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "name", "is_host")
    fieldsets = (
        (
            _("기본정보"),
            {
                "fields": ("username", "password"),
            },
        ),
        (
            _("프로파일"),
            {
                "fields": ("email", "name", "is_host"),
            },
        ),
        (
            _("권한"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("중요한 일자들"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
