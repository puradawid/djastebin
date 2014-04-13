from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from hashids import Hashids
import time
import settings
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from notifications import notify
import re
from django.core.context_processors import request

class Paste(models.Model):
    SYNTAX_CHOICES = (
            ('NONE', 'None'),
            ('JAVA', 'Java'),
            ('PYTHON', 'Python'),
    )
    VISIBILITY_CHOICES = (
            ('PUBLIC', 'Public'),
            ('UNLISTED', 'Unlisted'),
            ('PRIVATE', 'Private'),
    )
    
    title = models.CharField(max_length=70, default='Untitled')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hash = models.SlugField(editable=False, primary_key=True)
    syntax = models.CharField(max_length=20, choices=SYNTAX_CHOICES)
    visibility = models.CharField(max_length=8, choices=VISIBILITY_CHOICES)
    expire_date = models.DateTimeField(null=True, blank=True, default=None)
    hits = models.IntegerField(default=0)
    size = models.FloatField(default=0.00)
    author = models.ForeignKey(User, null=True, blank=True, default=None)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('show_paste', args=[str(self.hash)])

    def save(self, *args, **kwargs):
        if not self.hash:
            hashids = Hashids(settings.SECRET_KEY)
            self.hash = hashids.encrypt(int(round(time.time()*10000)))
        
        super(Paste, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
    
class Comment(MPTTModel):
    created = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    paste = models.ForeignKey(Paste)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return "%s#%s" % (reverse('show_paste', args=[str(self.paste.pk)]), self.pk) 

    class MPTTMeta:
        order_insertion_by = ['created']
        
        
@receiver(post_save, sender=Comment)
def send_comment_notification(sender, created, instance, **kwargs):
    if created:
        iter = set(re.findall("(?: |^)@([\w_-]+)", instance.content))
        for i in iter:
            try:
                user_found = User.objects.get(username=i)
                if user_found != instance.author:
                    notify.send(instance.author, recipient=user_found,verb='used your name', action_object=instance, target=instance.paste)
            except User.DoesNotExist:
                pass

