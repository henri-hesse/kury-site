from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from .forms import *

def admin_index(request):
  if request.method == 'POST':
    form = UserForm(request.POST)

    if form.is_valid():
      form.save()

      messages.success(request, 'New user created!')

      return redirect(reverse('users:admin_index'))
    else:
      messages.error(request, 'New user not saved!')
  else:
    form = UserForm()

  return render(request, 'users/admin/index.html', {
    'form': form,
    'users': User.objects.all(),
  })

def admin_edit(request, pk):
  user = get_object_or_404(User, pk=pk)

  if request.method == 'POST':
    form = UserForm(request.POST, instance=user)

    if form.is_valid():
      form.save()
      messages.success(request, 'User saved!')

      return redirect(reverse('users:admin_index'))
    else:
      messages.error(request, 'User not saved!')
  else:
    form = UserForm(instance=user)

  return render(request, 'users/admin/edit.html', {
    'form': form,
    'user': user
  })

def admin_delete(request, pk):
  user = get_object_or_404(User, pk=pk)

  if request.method == 'POST':
    user.delete()
    messages.success(request, 'User deleted!')

    return redirect(reverse('users:admin_index'))

  raise Http404('Not a POST request')
