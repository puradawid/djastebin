# ./apps/pastes/forms.py

# Django imports
from django import forms
from apps.pastes.models import Paste

# Utilities import
from datetime import date, timedelta

class PasteForm(forms.ModelForm):
   class Meta:
       model = Paste
       fields = ['title', 'content', 'language', 'visibility']
       labels = { 'content' : 'New Paste'}

   EXPIRATION_CHOICES = (
      ('0', 'Never'),
      ('5', '5 minutes'),
      ('10', '10 minutes'),
   )

   visibility = forms.ChoiceField(choices=Paste.VISIBILITY_CHOICES) 
   expiration = forms.ChoiceField(choices=EXPIRATION_CHOICES)
   
   def save(self):
       result = super(forms.ModelForm, self).save(commit=False)
       time = int(self.cleaned_data['expiration'])
       if time == 0:
          time = None
       else:
          time = date.today() + timedelta(minutes=time)
       result.expire_date = time 
       result.save()
       return result


