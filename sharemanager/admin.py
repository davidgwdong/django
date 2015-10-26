from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from sharemanager.models import XPUser

class XPUserAdmin(UserAdmin):
    model = XPUser

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('gcm_token',)}),
    )

admin.site.register(XPUser, XPUserAdmin)
