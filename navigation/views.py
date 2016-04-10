from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from .models import *
from .forms import *

def admin_index(request):
  if request.method == 'POST':
    form = ItemForm(request.POST)

    if request.is_ajax():
      return render(request, 'navigation/admin/item/form.html', {
        'form': form,
        'skip_errors': True,
      })

    if form.is_valid():
      form.save()
      messages.success(request, 'New item created!')

      return redirect(reverse('navigation:admin_index'))
    else:
      messages.error(request, 'New item not saved!')
  else:
    form = ItemForm()

  return render(request, 'navigation/admin/item/index.html', {
    'items': Item.objects.top_level(),
    'form': form,
  })

def admin_edit(request, pk):
  item = get_object_or_404(Item, pk=pk)

  if request.method == 'POST':
    form = ItemForm(request.POST, instance=item)

    if request.is_ajax():
      return render(request, 'navigation/admin/item/form.html', {
        'form': form,
        'skip_errors': True,
      })

    if form.is_valid():
      form.save()
      messages.success(request, 'Item updated!')

      return redirect(reverse('navigation:admin_index'))
    else:
      messages.error(request, 'Item not updated!')
  else:
    form = ItemForm(instance=item)

  return render(request, 'navigation/admin/item/edit.html', {
    'form': form,
    'item': item
  })

def admin_delete(request, pk):
  item = get_object_or_404(Item, pk=pk)

  if request.method == 'POST':
    item.delete()
    messages.success(request, 'Item deleted!')

    return redirect(reverse('navigation:admin_index'))

  raise Http404('Not a POST request')
