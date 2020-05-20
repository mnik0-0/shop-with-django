from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', })
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', })

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='password')

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', })


class ChangeSlugForm(forms.ModelForm):
    slug = forms.SlugField(required=True)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        slug = slugify(slug)
        if UserProfile.objects.filter(slug__iexact=slug).count():
            raise ValidationError('Slug is in use')
        return slug

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget = forms.TextInput(attrs={'class': 'form-control', })

    class Meta:
        model = models.UserProfile
        fields = ['slug']
