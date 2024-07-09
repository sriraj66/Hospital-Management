# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import *

class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label=_("Username"),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        
        return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'address', 'city', 'state', 'pincode']
        

class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if self.user is None:
            raise ValueError("User must be provided to the form")
        super(BlogForm, self).__init__(*args, **kwargs)

    def save(self, is_draft=False, commit=True):
        instance = super(BlogForm, self).save(commit=False)
        instance.user = self.user
        instance.is_draft = is_draft
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Blog
        fields = ['title', 'image', 'cat', 'summary', 'content']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control", "required": 'true'}),
            'image': forms.ClearableFileInput(attrs={"class": "form-control"}),
            'cat': forms.Select(choices=CATOGORIES, attrs={"class": "form-control"}),
            'summary': forms.Textarea(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control","placeholder": "Write as ## Markdown text"}),
        }

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CommentForm, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Comments
        fields = ['text',]
        widgets = {
            'text': forms.Textarea(attrs={"class": "form-control","required": 'true','placeholder':'Enter your comments'}),
            }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['cause', 'date', 'start_time']
        widgets = {
            'cause': forms.TextInput(attrs={"class": "form-control", "required": 'true'}),
            'date': forms.DateInput(attrs={"class": "form-control", "type": "date", "required": 'true'}),
            'start_time': forms.TimeInput(attrs={"class": "form-control", "type": "time", "required": 'true'}),
        }
