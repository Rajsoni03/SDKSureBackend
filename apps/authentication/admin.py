from django.contrib import admin

from .models import User, UserBoardAssignment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_active", "is_staff", "date_joined")
    search_fields = ("email", "username")
    list_filter = ("role", "is_active", "is_staff")


@admin.register(UserBoardAssignment)
class UserBoardAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "board", "assigned_at", "assigned_by")
    search_fields = ("user__email", "board__name")

