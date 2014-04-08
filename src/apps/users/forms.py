from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django.contrib.auth.hashers import make_password
from apps.users.models import Settings
from apps.pastes.models import Paste

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That username is already taken")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("That email is already in use")
        return email
    
class ProfileEditForm(ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank if don\'t want to change'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Your first name'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Your last name'}))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if (email != self.instance.email and User.objects.filter(email=email).exists()):
            raise forms.ValidationError("That email is already in use")
        return email
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) == 0:
            password = self.instance.password
        else:
            password = make_password(self.cleaned_data['password'])
        return password
    
class SettingsChangeForm(ModelForm):
    default_syntax = forms.ChoiceField(choices=Paste.SYNTAX_CHOICES)
    default_visibility = forms.ChoiceField(choices=Paste.VISIBILITY_CHOICES)
    default_expiration = forms.ChoiceField(choices=Settings.EXPIRATION_CHOICES)
    
    class Meta:
        model = Settings
        fiels = ['default_syntax', 'default_visibility', 'default_expiration']
        
    def clean_default_syntax(self):
        default_syntax = self.cleaned_data['default_syntax']
        return default_syntax
    
    def clean_default_visibility(self):
        default_visibility = self.cleaned_data['default_visibility']
        return default_visibility
    
    def clean_default_expiration(self):
        default_expiration = self.cleaned_data['default_expiration']
        return default_expiration