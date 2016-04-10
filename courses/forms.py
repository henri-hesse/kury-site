from django import forms
from .models import *

class CourseForm(forms.ModelForm):

  class Meta:
    model = Course
    fields = ('title', 'description', 'image')
    widgets = {
      'title': forms.TextInput(
        attrs = { 'class': 'form-control' }
      ),
      'description': forms.Textarea(
        attrs = {
          'class': 'form-control',
          'rows': 15,
        }
      )
    }

EventFormSet = forms.inlineformset_factory(Course, CourseEvent,
  fields = ('datetime', 'store_link'),
  widgets = {
    'datetime': forms.TextInput(
      attrs = {
        'class': 'form-control',
        'placeholder': 'VVVV-KK-PP TT:MM'
      }
    ),
    'store_link': forms.TextInput(
      attrs = {
        'class': 'form-control'
      }
    )
  }
)