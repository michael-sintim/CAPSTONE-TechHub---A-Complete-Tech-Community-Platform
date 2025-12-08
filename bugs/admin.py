from django.contrib import admin
from .models import Bug,BugHistory
# Register your models here.

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('title','status','priority','bug','changed_by','timestamp')
    list_filter = ('status','priority')
    date_hierarchy = 'created_at'
    list_per_page = 10

@admin.register(BugHistory)
class BugHistoryAdmin(admin.ModelAdmin):
    list_display = ('old_status','new_status')
    list_filter = ('old_status','new_status')
    search_fields = ('old_status','new_status')
