from django.contrib import admin
# This user class is actually used to customize the custom admin model
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','username', 'first_name', 'last_name','last_login', 'is_active', 'date_joined',)
    list_display_links = (
        'email',
        'username',
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    ordering = ('-date_joined',)
    # for one to use custom UserAdmin, one needs to use the FILTER_HORIZONTAL and lIST_FILTER
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
# admin.site.register(MyAccountManager)
