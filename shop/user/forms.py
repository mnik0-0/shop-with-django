from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'Oops'})

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.model = get_user_model()
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control', })
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', })

    class Meta:
        model = get_user_model()
        fields = ("email", "name", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if self.model.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class LoginForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', })
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control', })


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


class ChangeNameForm(forms.ModelForm):

    name = forms.CharField(required=True, max_length=20)

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', })

    class Meta:
        model = get_user_model()
        fields = ['name']
