from django.db import models
from django.contrib.auth.models import User
from apps.paste.models import Paste

class Comment(models.Model):
    created = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    paste = models.ForeignKey(Paste)
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    
    def __unicode__(self):
        return self.date
