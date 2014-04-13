from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from hashids import Hashids

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
    hash = models.SlugField()
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
        if not self.id:
            super(Paste, self).save(*args, **kwargs)
            self.hash = Hashids().encrypt(self.id)
            self.save()
        else:
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
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('show_paste', args=[str(self.pk)])
    
    def get_content(self):
        if self.deleted == False:
            return self.content
        else:
            return '[deleted by administrator]'
    
    class MPTTMeta:
        order_insertion_by = ['created']
        
    def __unicode__(self):
        if len(self.content) < 50:
            return self.content + '...'
        else:
            return self.content[50:] + '...'

