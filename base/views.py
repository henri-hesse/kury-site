from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from .models import *
from carousel.models import Image

def landing_page(request):
  return render(request, 'base/landing_page.html', {
  	'carousel_images': Image.objects.all()
  })

def staff(request):
  return render(request, 'base/staff.html', {
    'users': User.objects.all(),
  })