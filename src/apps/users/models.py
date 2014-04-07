from django.db import models
from django.contrib.auth.models import User
from apps.pastes.models import Paste

class Settings(models.Model):
    # Temporary data
    EXPIRATION_CHOICES = (
      ('0', 'Never'),
      ('5', '5 minutes'),
      ('10', '10 minutes'),
    )
    
    default_visibility =  models.CharField(max_length=8, choices=Paste.VISIBILITY_CHOICES)
    default_syntax = models.CharField(max_length=20, choices=Paste.SYNTAX_CHOICES)
    default_expiration = models.CharField(max_length=2, choices=EXPIRATION_CHOICES)
    
class Account(models.Model):
    user = models.OneToOneField(User)
    settings = models.OneToOneField(Settings)