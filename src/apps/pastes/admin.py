from django.contrib import admin
from apps.pastes.models import Paste
from apps.pastes.models import Comment
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse

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


class CommentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    
    actions = ['custom_delete_selected']
    def custom_delete_selected(self, request, queryset):
        for comment in queryset.all():
            comment.deleted = True
            comment.save()
    custom_delete_selected.short_description = "Delete selected items"
    
    def get_actions(self, request):
        actions = super(CommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    readonly_fields = ['author', 'paste']
    fields = ['author', 'paste', 'content', 'deleted']
    list_display = ['__unicode__', 'author', 'created', 'paste', 'deleted']
    
admin.site.register(Comment, CommentAdmin)