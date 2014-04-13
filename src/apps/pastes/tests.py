from django.test import TestCase
from django.contrib.auth.models import User
from apps.pastes.forms import CommentForm
from apps.pastes.models import Paste, Comment

class CommentFormTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='default', password='pass', email='email')
        user_second = User.objects.create(username='default_second', password='pass', email='email')
        paste = Paste.objects.create(content='foo', hash='foo', syntax='NONE', visibility='PUBLIC', author=user)
        
        comment_first_lv = Comment.objects.create(content='foo', author=user, paste=paste, parent=None)
        comment_second_lv = Comment.objects.create(content='foo', author=user, paste=paste, parent=comment_first_lv)
        comment_third_lv = Comment.objects.create(content='foo @default @default_second', author=user_second, paste=paste, parent=comment_second_lv)
        
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
        paste = Paste.objects.get()
        data = { 'content': 'foo', 'author': user, 'paste': paste, 'parent': None }
        form = CommentForm(data)
        self.assertTrue(form.is_valid())
        
        # Submit valid data with parent
        user = User.objects.get(pk=1)
        paste = Paste.objects.get()
        data = { 'content': 'foo', 'author': user, 'paste': paste, 'parent': comment_fourth_lv }
        form = CommentForm(data)
        self.assertTrue(form.is_valid())
        
    def test_notifications(self):
        "Check notification existance"
        
        # default user should have 1 notification
        self.assertEqual(User.objects.get(username='default').notifications.unread().count(), 1)
        
        # default_second user should not have any notifications
        self.assertEqual(User.objects.get(username='default_second').notifications.unread().count(), 0)
        
        # defaults user notification should reffer to comment_third_lv
        
        comment_fourth_lv = Comment.objects.get(pk=3)
        self.assertEqual(User.objects.get(username='default').notifications.unread().get().action_object, comment_fourth_lv)