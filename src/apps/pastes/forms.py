# ./apps/pastes/forms.py

# Django imports
from django import forms
from apps.pastes.models import Paste

# Utilities import
from datetime import timedelta
from django.utils import timezone
from apps.users.models import Settings

class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['title', 'content', 'syntax', 'visibility']

    syntax = forms.ChoiceField(choices=Paste.SYNTAX_CHOICES)
    visibility = forms.ChoiceField(choices=Paste.VISIBILITY_CHOICES) 
    expiration = forms.ChoiceField(choices=Settings.EXPIRATION_CHOICES)

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
        self.fields['expiration'] = forms.ChoiceField(choices=(('-1', 'Don\'t change'),) + Settings.EXPIRATION_CHOICES)
        