from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from hashids import Hashids
import time
import settings
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from notifications import notify
import re

class Paste(models.Model):
    SYNTAX_CHOICES = (
            ('NONE', _('None')),
            ('JAVA', 'Java'),
            ('PYTHON', 'Python'),
    )
    VISIBILITY_CHOICES = (
            ('PUBLIC', _('Public')),
            ('UNLISTED', _('Unlisted')),
            ('PRIVATE', _('Private')),
    )
    
    title = models.CharField(_('Title'),max_length=70, default='Untitled')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hash = models.CharField(max_length=15, editable=False, primary_key=True)
    syntax = models.CharField(_('Syntax'), max_length=20, choices=SYNTAX_CHOICES)
    visibility = models.CharField(_('Visibility'), max_length=8, choices=VISIBILITY_CHOICES)
    expire_date = models.DateTimeField(null=True, blank=True, default=None)
    hits = models.IntegerField(default=0)
    size = models.FloatField(default=0.00)
    author = models.ForeignKey(User, null=True, blank=True, default=None)
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('show_paste', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        if not self.pk:
            hashids = Hashids(settings.SECRET_KEY)
            self.hash = hashids.encrypt(int(round(time.time()*10000)))
        
        super(Paste, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class Comment(MPTTModel):
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    paste = models.ForeignKey(Paste)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    deleted = models.BooleanField(default=False)
    
    def get_content(self):
        if self.deleted == False:
            return self.content
        else:
            return '[deleted by administrator]'
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return "%s#%s" % (reverse('show_paste', args=[str(self.paste.pk)]), self.pk) 

    class MPTTMeta:
        order_insertion_by = ['created']
        
    def __unicode__(self):
        if len(self.content) < 50:
            return self.content + '...'
        else:
            return self.content[50:] + '...'
        
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

