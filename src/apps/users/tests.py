from django.test import TestCase
from django.contrib.auth.models import User
from apps.users.models import Settings, Account
from apps.users.forms import ProfileEditForm
from apps.pastes.models import Paste
from apps.users.views import SettingsView

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
        
class ProfileEditFormTestCase(TestCase):
        
    def setUp(self):
        user = User.objects.create_user(username='john@example.com', password='ExtremelyHardPassword', email='john@example.com')

    def test_invalid_form(self):
        "Submit invalid data"
        
        # Submit no data
        form = ProfileEditForm()
        self.assertFalse(form.is_valid())
        
        # Submit invalid data
        data = { 'email': 'foo' }
        form = ProfileEditForm(data=data)
        self.assertFalse(form.is_valid())
        
        # Submit existing data (email)
        data = { 'email': 'john@example.com' }
        form = ProfileEditForm(data = data)
        self.assertFalse(form.is_valid())
        
    def test_valid_form(self):
        "Submit valid data"
        
        # Submit valid data
        data = { 'email': 'johnny@example.com', 'first_name': 'John', 'last_name': 'Smith', 'password':  'ExtremelyHardPassword'}
        form = ProfileEditForm(data = data)
        self.assertTrue(form.is_valid())