from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from .forms import *

@login_required
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

@login_required
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

@login_required
def admin_delete(request, pk):
  user = get_object_or_404(User, pk=pk)

  if request.method == 'POST':
    user.delete()
    messages.success(request, 'User deleted!')

    return redirect(reverse('users:admin_index'))

  raise Http404('Not a POST request')

def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)

    if form.login(request):
      messages.success(request, 'Welcome!')

      return redirect(reverse('navigation:admin_index'))

    else:
      messages.error(request, 'Username or password incorrect!')
  else:
    form = LoginForm()

  return render(request, 'users/admin/login.html', {
    'form': form
  })

def logout(request):
  logout_user(request)
  messages.success(request, 'Logged out!')

  return redirect('base:landing_page')