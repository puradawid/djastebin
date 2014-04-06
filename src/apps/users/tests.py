from django.test import TestCase
from django.contrib.auth.models import User
from apps.users.models import Settings, Account

class AccountTestCase(TestCase):
    
    username = 'foo'
    password = 'SuperStrongPassword'
    default_syntax = 'NONE'
    default_visibility = 'PUBLIC'
    
    def setUp(self):
        user = User.objects.create_user(username=self.username, password=self.password)
        settings = Settings.objects.create(default_syntax=self.default_syntax, default_visibility=self.default_visibility)
        account = Account.objects.create(user = user, settings = settings)
    
    def test_db(self):
        user = User.objects.get(username=self.username)
        settings = Settings.objects.get(id=1)
        
        self.assertEqual(user.username, self.username)
        self.assertEqual(settings.default_syntax, self.default_syntax)
        self.assertEqual(settings.default_visibility, self.default_visibility)
        
    def test_account_relations(self):
        user = User.objects.get(username=self.username)
        self.assertEqual(user.account.settings.default_syntax, self.default_syntax)
        self.assertEqual(user.account.settings.default_visibility, self.default_visibility)