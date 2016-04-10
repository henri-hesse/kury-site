from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from .models import *
from carousel.models import Image

def landing_page(request):
  return render(request, 'base/landing_page.html', {
  	'carousel_images': Image.objects.all()
  })
