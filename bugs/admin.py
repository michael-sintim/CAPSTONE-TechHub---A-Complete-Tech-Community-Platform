from django.contrib import admin
from .models import Bug,BugHistory
# Register your models here.

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('title','status','priority','project','reporter')
    list_filter = ('status','priority','project__title')
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ("Bug Details",{
            'fields': ('title','description','file_attachment')
        }),

        ("Status",{
            'fields': ('status','priority','project')
        }),
        (
            'People',{'fields':('reporter','assigned_to')}
        ))

@admin.register(BugHistory)
class BugHistoryAdmin(admin.ModelAdmin):
    list_display = ('bug','changed_by','timestamp')
    list_filter = ('old_status','new_status')
    search_fields = ('old_status','new_status')
    readonly_fields = ('bug', 'old_status', 'new_status', 'changed_by', 'timestamp')

