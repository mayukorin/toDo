from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SiteUser
# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = SiteUser
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('flag',)}),)
    list_display = ['username', 'email', 'flag']
 
 
admin.site.register(SiteUser, CustomUserAdmin)