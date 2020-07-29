from django import forms
from . import models


class ItemCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'rows': '3'})
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', })
        self.fields['tag'].widget = forms.Select(attrs={'class': 'form-control', },
                                                 choices=models.LocalTag.objects.all().values_list('id', 'title'))
        self.fields['price'].widget = forms.TextInput(attrs={'class': 'form-control', })

    class Meta:
        model = models.Item
        fields = ['title', 'description', 'tag', 'price']


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


class GlobalTagCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'rows': '3'})

    class Meta:
        model = models.GlobalTag
        fields = ['title']


class LocalTagCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={'class': 'form-control', 'rows': '3'})
        self.fields['global_tag'].widget = forms.Select(attrs={'class': 'form-control', },
                                                        choices=models.GlobalTag.objects.all().values_list('id',
                                                                                                           'title'))

    class Meta:
        model = models.LocalTag
        fields = ['title', 'global_tag']


class SearchForm(forms.Form):

    search = forms.CharField(max_length=25, required=False)
    min = forms.IntegerField(min_value=0, required=False)
    max = forms.IntegerField(min_value=0, required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['search'].widget = forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Search'})
        self.fields['min'].widget = forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Min'})
        self.fields['max'].widget = forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Max'})
