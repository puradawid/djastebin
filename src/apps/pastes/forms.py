# ./apps/pastes/forms.py

# Django imports
from django import forms
from apps.pastes.models import Paste

# Utilities import
from datetime import datetime, timedelta

class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['title', 'content', 'syntax', 'visibility']

    EXPIRATION_CHOICES = [
        ('0', 'Never'),
        ('5', '5 minutes'),
        ('10', '10 minutes'),
    ]

    syntax = forms.ChoiceField(choices=Paste.SYNTAX_CHOICES)
    visibility = forms.ChoiceField(choices=Paste.VISIBILITY_CHOICES) 
    expiration = forms.ChoiceField(choices=EXPIRATION_CHOICES)

    def save(self):
        result = super(PasteForm, self).save(commit=False)

        time = int(self.cleaned_data['expiration'])
        if time == 0:
            time = None
        elif time == -1:
            time = result.expire_date
        else:
            time = datetime.now() + timedelta(minutes=time)
        result.expire_date = time

        result.save(force_insert=False)
        return result
    
class PasteFormEdit(PasteForm):    
    EXPIRATION_CHOICES = [
        ('-1', 'Don\'t change'),
        ('0', 'Never'),
        ('5', '5 minutes'),
        ('10', '10 minutes'),
    ]
    def __init__(self, *args, **kwargs):
        super(PasteFormEdit, self).__init__(*args, **kwargs)
        self.fields['expiration'] = forms.ChoiceField(choices=self.EXPIRATION_CHOICES)
        