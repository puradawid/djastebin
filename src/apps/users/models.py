from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.pastes.models import Paste
from django.db.models.signals import post_save

class Settings(models.Model):
    # Temporary data
    EXPIRATION_CHOICES = (
      ('0', _('Never')),
      ('5', _('5 minutes')),
      ('10', _('10 minutes')),
    )
    
    visibility =  models.CharField(_('Visibility'), max_length=8, choices=Paste.VISIBILITY_CHOICES, default=(Paste.VISIBILITY_CHOICES[0])[0])
    syntax = models.CharField(_('Syntax'), max_length=20, choices=Paste.SYNTAX_CHOICES, default=(Paste.SYNTAX_CHOICES[0])[0])
    expiration = models.CharField(_('Expiration'), max_length=2, choices=EXPIRATION_CHOICES, default=(EXPIRATION_CHOICES[0])[0])
    
class Account(models.Model):
    user = models.OneToOneField(User)
    settings = models.OneToOneField(Settings)
    
def create_account_for_new_user(sender, created, instance, **kwargs):
    if created:
        settings = Settings.objects.create()
        account = Account.objects.create(user=instance, settings=settings)
        
post_save.connect(create_account_for_new_user, User, dispatch_uid='create_account_for_new_user')
