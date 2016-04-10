from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from .models import *
from .forms import *

def admin_index(request):
  if request.method == 'POST':
    form = PageForm(request.POST)

    if form.is_valid():
      form.save()

      messages.success(request, 'New page created!')

      return redirect(reverse('pages:admin_index'))
    else:
      messages.error(request, 'New page not saved!')
  else:
    form = PageForm()

  return render(request, 'pages/admin/index.html', {
    'form': form,
    'pages': Page.objects.all(),
  })

def admin_edit(request, pk):
  page = get_object_or_404(Page, pk=pk)

  if request.method == 'POST':
    form = PageForm(request.POST, instance=page)

    if form.is_valid():
      form.save()
      messages.success(request, 'Page saved!')

      return redirect(reverse('pages:admin_index'))
    else:
      messages.error(request, 'Page not saved!')
  else:
    form = PageForm(instance=page)

  return render(request, 'pages/admin/edit.html', {
    'form': form,
    'page': page
  })

def admin_delete(request, pk):
  page = get_object_or_404(Page, pk=pk)

  if request.method == 'POST':
    page.delete()
    messages.success(request, 'Page deleted!')

    return redirect(reverse('pages:admin_index'))

  raise Http404('Not a POST request')

def show_page(request, pk, slug):
  return render(request, 'pages/show.html', {
    'page': get_object_or_404(Page, pk=pk)
  })
