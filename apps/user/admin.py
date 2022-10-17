from django.contrib import admin
from apps.accounts.models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'role']


admin.site.register(User, UserAdmin)
