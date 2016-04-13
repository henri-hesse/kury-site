from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

@login_required
def admin_index(request):
  if request.method == 'POST':
    form = ImageForm(request.POST, request.FILES)

    if form.is_valid():
      form.save()

      messages.success(request, 'New image created!')

      return redirect(reverse('carousel:admin_index'))
    else:
      messages.error(request, 'New image not saved!')
  else:
    form = ImageForm()

  return render(request, 'carousel/admin/index.html', {
    'form': form,
    'images': Image.objects.all(),
  })

@login_required
def admin_edit(request, pk):
  image = get_object_or_404(Image, pk=pk)

  if request.method == 'POST':
    form = ImageForm(request.POST, request.FILES, instance=image)

    if form.is_valid():
      form.save()

      messages.success(request, 'Image saved!')

      return redirect(reverse('carousel:admin_index'))
    else:
      messages.error(request, 'Image not saved!')
  else:
    form = ImageForm(instance=image)

  return render(request, 'carousel/admin/edit.html', {
    'form': form,
    'image': image
  })

@login_required
def admin_delete(request, pk):
  image = get_object_or_404(Image, pk=pk)

  if request.method == 'POST':
    image.delete()
    messages.success(request, 'Image deleted!')

    return redirect(reverse('carousel:admin_index'))

  raise Http404('Not a POST request')

@login_required
def admin_move_up(request, pk):
  image = get_object_or_404(Image, pk=pk)

  if image.order_number == 0:
    raise Http404('Image already the first image')

  if request.method == 'POST':
    image.reorder(image.order_number - 1)

    return redirect(reverse('carousel:admin_index'))

  raise Http404('Not a POST request')

@login_required
def admin_move_down(request, pk):
  image = get_object_or_404(Image, pk=pk)

  if image.order_number == Image.max_order_number():
    raise Http404('Image already the last image')

  if request.method == 'POST':
    image.reorder(image.order_number + 1)
    
    return redirect(reverse('carousel:admin_index'))

  raise Http404('Not a POST request')