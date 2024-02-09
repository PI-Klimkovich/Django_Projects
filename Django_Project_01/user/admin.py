from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = ['username', 'first_name', 'last_name', 'count_note', "is_active"]
    search_fields = ['username', 'first_name']
    actions = ["block_user", "unlock_user"]
    list_editable = ("is_active",)

    @admin.display(description="Counts notes")
    def count_note(self, obj):
        return obj.note_set.count()

    @admin.action(description='Block User')
    def block_user(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Unlock User')
    def unlock_user(self, request, queryset):
        queryset.update(is_active=True)

    fieldsets = (
        # 1  tuple(None, dict)
        (None, {"fields": ("username", "password")}),

        # 2  tuple(str, dict)
        ("Персональная информация", {"fields": ("first_name", "last_name", "email", "phone", "country")}),

        # 3  tuple(str, dict)
        (
            "Права пользователя",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),

        # 4  tuple(str, dict)
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )
