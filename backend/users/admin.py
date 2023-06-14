from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.user import User


class CustomUserAdmin(UserAdmin):

    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
    ordering = ('pk',)


admin.site.register(User, CustomUserAdmin)
