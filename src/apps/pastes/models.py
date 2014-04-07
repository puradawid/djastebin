from django.db import models
from django.contrib.auth.models import User

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
    hash = models.CharField(max_length=100) # Temporary length
    syntax = models.CharField(max_length=20, choices=SYNTAX_CHOICES)
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    expire_date = models.DateTimeField(null=True, blank=True, default=None)
    hits = models.IntegerField(default=0)
    size = models.FloatField(default=0.00)
    author = models.ForeignKey(User, null=True, blank=True, default=None)
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('show_paste', args=[str(self.pk)])
    
class Comment(models.Model):
    created = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    paste = models.ForeignKey(Paste)
    parent = models.ForeignKey('self', null=True, blank=True, default=None)
    
    def __unicode__(self):
        return self.date

