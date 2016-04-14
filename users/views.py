from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout as logout_user
from .forms import *
from .models import *

@login_required
def admin_index(request):
  if request.method == 'POST':
    user_form = UserForm(request.POST)
    detail_form = DetailForm(request.POST, request.FILES)

    if user_form.is_valid() and detail_form.is_valid():
      user_form.save()

      detail_form.instance.user = user_form.instance
      detail_form.save()

      messages.success(request, 'New user created!')

      return redirect(reverse('users:admin_index'))
    else:
      messages.error(request, 'New user not saved!')
  else:
    user_form = UserForm()
    detail_form = DetailForm()

  return render(request, 'users/admin/index.html', {
    'user_form': user_form,
    'detail_form': detail_form,
    'users': User.objects.all(),
  })

@login_required
def admin_edit(request, pk):
  user = get_object_or_404(User, pk=pk)

  if request.method == 'POST':
    user_form = UserForm(request.POST, instance=user)
    detail_form = DetailForm(request.POST, request.FILES, instance=user.detail)

    if user_form.is_valid() and detail_form.is_valid():
      user_form.save()
      detail_form.save()
      messages.success(request, 'User saved!')

      return redirect(reverse('users:admin_index'))
    else:
      messages.error(request, 'User not saved!')
  else:
    user_form = UserForm(instance=user)
    detail_form = DetailForm(instance=user.detail)

  return render(request, 'users/admin/edit.html', {
    'user_form': user_form,
    'detail_form': detail_form,
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