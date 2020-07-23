from django import forms
from . import models


class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = forms.TextInput(attrs={'class': 'form-control rounded-0 border-0 py-4 bg-light'})

    class Meta:
        model = models.Message
        fields = ['text']
