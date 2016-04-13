from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class UserForm(forms.ModelForm):
  password_1 = forms.CharField(
    required = False,
    help_text = 'Choose a new password. Leave passwords empty if you do not want to change the password for existing user.',
    label = 'Password',
    widget = forms.PasswordInput(
      attrs = { 'class': 'form-control' }
    ),
  )
  password_2 = forms.CharField(
    required = False,
    help_text = 'Repeat the password',
    label = 'Password, again',
    widget = forms.PasswordInput(
      attrs = { 'class': 'form-control' }
    ),
  )

  class Meta:
    model = User
    fields = ('username',)
    widgets = {
      'username': forms.TextInput(
        attrs = { 'class': 'form-control' }
      )
    }

  def clean(self):
    cleaned_data = super(UserForm, self).clean()

    password_1 = cleaned_data.get('password_1')
    password_2 = cleaned_data.get('password_2')

    if self.instance.pk is None and password_1 == '':
      error = 'Password is required'
      self.add_error('password_1', error)
      self.add_error('password_2', error)

    if (password_1 != '' or password_2 != '') and password_1 != password_2:
      error = 'Passwords must match'
      self.add_error('password_1', error)
      self.add_error('password_2', error)

  def save(self, *args, **kwargs):
    password_1 = self.cleaned_data['password_1']

    if password_1 != '':
      self.instance.set_password(password_1)

    return super(UserForm, self).save(*args, **kwargs)

class LoginForm(forms.Form):
  username = forms.CharField(
    widget = forms.TextInput(
      attrs = { 'class': 'form-control' }
    )
  )

  password = forms.CharField(
    widget = forms.PasswordInput(
      attrs = { 'class': 'form-control' }
    )
  )

  def login(self, request):
    # Only to get access to cleaned_data
    self.is_valid()
    user = authenticate(username = self.cleaned_data.get('username'), password = self.cleaned_data.get('password'))

    if user is not None:
      login(request, user)
      return True

    return False