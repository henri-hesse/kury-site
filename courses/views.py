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
    form = CourseForm(request.POST, request.FILES)
    event_formset = EventFormSet(request.POST)

    if form.is_valid() and event_formset.is_valid():
      form.save()
      event_formset.save()

      messages.success(request, 'New course created!')

      return redirect(reverse('courses:admin_index'))
    else:
      messages.error(request, 'New course not saved!')
  else:
    form = CourseForm()
    event_formset = EventFormSet()

  return render(request, 'courses/admin/index.html', {
    'form': form,
    'event_formset': event_formset,
    'courses': Course.objects.all(),
  })

@login_required
def admin_edit(request, pk):
  course = get_object_or_404(Course, pk=pk)

  if request.method == 'POST':
    form = CourseForm(request.POST, request.FILES, instance=course)
    event_formset = EventFormSet(request.POST, instance=course)

    if form.is_valid() and event_formset.is_valid():
      form.save()
      event_formset.save()

      messages.success(request, 'Course saved!')

      return redirect(reverse('courses:admin_index'))
    else:
      messages.error(request, 'Course not saved!')
  else:
    form = CourseForm(instance=course)
    event_formset = EventFormSet(instance=course)

  return render(request, 'courses/admin/edit.html', {
    'form': form,
    'event_formset': event_formset,
    'course': course
  })

@login_required
def admin_delete(request, pk):
  course = get_object_or_404(Course, pk=pk)

  if request.method == 'POST':
    course.delete()
    messages.success(request, 'Course deleted!')

    return redirect(reverse('courses:admin_index'))

  raise Http404('Not a POST request')

def index(request):
  return render(request, 'courses/index.html', {
    'courses': Course.objects.visible()
  })

def show(request, pk):
  return render(request, 'courses/show.html', {
    'course': get_object_or_404(Course, pk=pk)
  })