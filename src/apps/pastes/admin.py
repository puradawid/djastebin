from django.contrib import admin
from apps.pastes.models import Paste

class PasteAdmin(admin.ModelAdmin):
    readonly_fields = ('hash', 'hits', 'size')
    list_display = ('title', 'created', 'hits', 'size')
    list_filter = ('created', 'visibility', 'syntax')
    search_fields = ('title', 'author')

admin.site.register(Paste, PasteAdmin)