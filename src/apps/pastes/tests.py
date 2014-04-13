from django.test import TestCase
from django.contrib.auth.models import User
from apps.pastes.forms import CommentForm
from apps.pastes.models import Paste, Comment

class CommentFormTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='default', password='pass', email='email')
        paste = Paste.objects.create(content='foo', pk='foo', syntax='NONE', visibility='PUBLIC', author=user)
        
        comment_first_lv = Comment.objects.create(content='foo', author=user, paste=paste, parent=None)
        comment_second_lv = Comment.objects.create(content='foo', author=user, paste=paste, parent=comment_first_lv)
        comment_third_lv = Comment.objects.create(content='foo', author=user, paste=paste, parent=comment_second_lv)
        
    def test_invalid_form(self):
        "Submit invalid data"
        
        # Submit empty form
        form = CommentForm()
        self.assertFalse(form.is_valid())
        
    def test_valid_form(self):
        "Submit valid data"
        
        comment_fourth_lv = Comment.objects.get(pk=3)
        
        # Submit valid data without parent
        user = User.objects.get(pk=1)
        paste = Paste.objects.get(pk=1)
        data = { 'content': 'foo', 'author': user, 'paste': paste, 'parent': None }
        form = CommentForm(data)
        self.assertTrue(form.is_valid())
        
        # Submit valid data with parent
        user = User.objects.get(pk=1)
        paste = Paste.objects.get(pk=1)
        data = { 'content': 'foo', 'author': user, 'paste': paste, 'parent': comment_fourth_lv }
        form = CommentForm(data)
        self.assertTrue(form.is_valid())
        
