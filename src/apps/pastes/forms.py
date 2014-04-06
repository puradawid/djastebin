# ./apps/pastes/forms.py

# Django imports
from django import forms
from apps.pastes.models import Paste

class CreatePasteForm(forms.Form):
   EXPIRATION_CHOICES = (
	('0', 'Never'),
	('5', '5 minutes'),
	('10', '10 minutes'),
   )
   VISIBILITY_CHOICES = Paste.VISIBILITY_CHOICES
   SYNTAX_CHOICES = Paste.LANGUAGE_CHOICES #when merged has to be changed to SYNTAX

   title = forms.CharField(label="Name", max_length=100, required=False) 
   content = forms.CharField(required=True, widget=forms.Textarea)
   expiration = forms.ChoiceField(choices=EXPIRATION_CHOICES)
   syntax = forms.ChoiceField(label="Syntax Highlighting", choices=SYNTAX_CHOICES)
   visibility = forms.ChoiceField(choices=VISIBILITY_CHOICES)
