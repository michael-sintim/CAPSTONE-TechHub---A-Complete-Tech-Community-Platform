from django.contrib import admin
from .models import Project,ProjectImage
# Register your models here.


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1 


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','status','user','category','is_public','due_date',)
    list_filter = ('status','category','user__username')
    search_fields = ("title","description",'status')
    readonly_fields= ('slug','created_at','updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 20 
    inlines = [ProjectImageInline]
