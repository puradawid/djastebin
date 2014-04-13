from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from hashids import Hashids
import time
import settings

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
    created = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    paste = models.ForeignKey(Paste)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('show_paste', args=[str(self.pk)])

    class MPTTMeta:
        order_insertion_by = ['created']

