from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username','get_email','urls','bio')
    list_filter  = ('is_active',)
    search_fields = ('bio',)
    date_hierarchy = 'created_at'

    def get_username(self,obj):
        return obj.user.username
    get_username.short_desciption = "Username"
    
    def get_email(self,obj):
        return obj.user.email
    get_email.short_description = 'Email '