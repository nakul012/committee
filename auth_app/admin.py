from django.contrib import admin
from auth_app.models import Account
from django.contrib.auth.models import Group


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = (['password'])
    list_display = ("email", "password", "is_active", "is_admin")


admin.site.unregister(Group)