from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('phone_number', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)