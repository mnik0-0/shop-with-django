from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class ItemCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'rows': '3'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', })
        self.fields['tag'].widget = forms.Select(attrs={'class': 'form-control', }, choices=models.LocalTag.objects.all().values_list('id', 'title'))

    class Meta:
        model = models.Item
        fields = ['title', 'description', 'tag']


class ItemImagesForm(forms.Form):
    photos = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['photos'].widget = forms.FileInput(attrs={'multiple': 'multiple', })

    def clean_photos(self):
        photos = [photo for photo in self.request.FILES.getlist('photos') if 'image' in photo.content_type]
        return photos

    def save_for(self, item):
        for image in self.cleaned_data['photos']:
            models.ItemPhoto(image=image, item=item).save()
        if len(self.cleaned_data['photos']) == 0:
            models.ItemPhoto(item=item).save()
