from django.db import models
from django.contrib.auth.models import User
from apps.pastes.models import Paste

class Settings(models.Model):
    default_visibility =  models.CharField(max_length=7, choices=Paste.VISIBILITY_CHOICES)
    default_syntax = models.CharField(max_length=20, choices=Paste.SYNTAX_CHOICES)

class Account(models.Model):
    user = models.OneToOneField(User)
    settings = models.OneToOneField(Settings)