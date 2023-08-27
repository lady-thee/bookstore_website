from django.contrib import admin
from .models import UserAccount


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'username',
        'is_active',
        'is_staff',
        'is_verified',
        'is_superuser',
        'password',
        'created_time',
        'last_login'
    ]

    list_display_links = ['email']


admin.site.register(UserAccount, UserAdmin)

