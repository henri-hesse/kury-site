from django import forms
from .models import *

class ImageForm(forms.ModelForm):

  class Meta:
    model = Image
    fields = ('caption', 'image')
    widgets = {
      'caption': forms.Textarea(
        attrs = {
          'class': 'form-control',
          'rows': 15,
        }
      )
    }