# ./apps/pastes/forms.py

# Django imports
from django import forms
from apps.pastes.models import Paste, Comment

# Utilities import
from django.forms.models import ModelForm
from datetime import timedelta
from django.utils import timezone
from apps.users.models import Settings
from django.utils.translation import ugettext as _

class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['title', 'content', 'syntax', 'visibility']

    syntax = forms.ChoiceField(label=_('Syntax'), choices=Paste.SYNTAX_CHOICES)
    visibility = forms.ChoiceField(label=_('Visibility'), choices=Paste.VISIBILITY_CHOICES) 
    expiration = forms.ChoiceField(label=_('Expiration'), choices=Settings.EXPIRATION_CHOICES)
    
    def save(self):
        result = super(PasteForm, self).save(commit=False)

        time = int(self.cleaned_data['expiration'])
        if time == 0:
            time = None
        elif time == -1:
            time = result.expire_date
        else:
            time = timezone.now() + timedelta(minutes=time)
        result.expire_date = time

        result.save(force_insert=False)
        return result

class PasteFormEdit(PasteForm):    
    def __init__(self, *args, **kwargs):
        super(PasteFormEdit, self).__init__(*args, **kwargs)       
        self.fields['expiration'] = forms.ChoiceField(choices=(('-1', _('Don\'t change')),) + Settings.EXPIRATION_CHOICES)
    
class CommentForm(ModelForm):
    comment_parent = forms.CharField(required=False, widget = forms.HiddenInput())
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))
    
    class Meta:
        model = Comment
        fields = ['content', 'comment_parent']
    
    def save(self, commit=True):
        result = super(forms.ModelForm, self).save(commit=False)
        
        pk = self.cleaned_data['comment_parent']

        if pk == '':
            result.parent = None
        else:
            result.parent = Comment.objects.get(pk=pk)
            if result.parent.level > 2:
                raise forms.ValidationError("Can't reply to comments on level more than 2")
            
        result.save()
        return result