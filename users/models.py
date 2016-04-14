from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Detail(models.Model):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
  )
  image = ProcessedImageField(
    upload_to = 'users/',
    processors = [ResizeToFill(400, 400)],
    format = 'JPEG',
    options = {'quality': 90},
    verbose_name = 'Profile picture',
    help_text = 'Pick up a image file from your computer. Image should be big enough so that it wont get scaled up by the system.'
  )
