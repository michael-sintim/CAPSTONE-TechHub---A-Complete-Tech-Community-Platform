from django.contrib import admin
from .models import Discussion
# Register your models here.

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('author','category','title','content')
    list_filter = ('author','category','title')
    search_fields = ('author__username','category__name')

    fieldsets = (
        ('Discussion',{'fields':('author','category','title','content')},
         ),
         ("Content",{'fields':('content','tags')})
         ("Engagement",{'fields':('parent','following', 'voting'),
                        'classes': ('collapse')})
         
    )