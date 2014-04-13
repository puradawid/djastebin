from django.contrib import admin
from apps.pastes.models import Paste

class PasteAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    fieldsets = [
        (None,          {'fields': ['content']}),
        ('Settings',    {'fields': ['title', 'syntax', 'visibility', 'expire_date']}),
    ]
    list_display = ('title', 'created', 'syntax', 'visibility', 'expire_date', 'hits', 'size')
    list_filter = ['created', 'syntax', 'visibility']
    search_fields = ['title']

admin.site.register(Paste, PasteAdmin)
