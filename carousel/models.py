from __future__ import unicode_literals
from django.db import models
import markdown

class Image(models.Model):
  order_number = models.PositiveIntegerField(
  	verbose_name = 'Order number of the image'
  )
  caption = models.TextField(
    blank = True,
    null = True,
  	verbose_name = 'Caption text for the image',
  	help_text = 'Text to show at the bottom of the image. You may use MarkDown here.'
  )
  image = models.ImageField(
  	upload_to = 'carousel/',
  	verbose_name = 'Image file',
  	help_text = 'Pick up a image file from your computer. Image should be big enough so that it wont get scaled up by the system.'
  )

  @classmethod
  def max_order_number(cls):
  	return Image.objects.all().aggregate(models.Max('order_number'))['order_number__max']

  def __unicode__(self):
    return self.caption

  class Meta:
    ordering = ['order_number']

  def __init__(self, *args, **kwargs):
    super(Image, self).__init__(*args, **kwargs)

    if not self.pk:
      self.to_the_end()

  def caption_html(self):
		return markdown.markdown(self.caption, extensions=['markdown.extensions.nl2br'])

  def delete(self, *args, **kwargs):
  	self.slice_off()
  	return super(Image, self).delete(*args, **kwargs)

  def to_the_end(self):
  	max_order_number = Image.max_order_number()

  	self.order_number = 0
  	if max_order_number is not None:
  		self.order_number = max_order_number + 1

  def reorder(self, new_order_number):
  	self.slice_off()
  	self.push_between(new_order_number)

  def slice_off(self):
  	Image.objects.filter(order_number__gt=self.order_number).update(order_number=models.F('order_number') - 1)

  def push_between(self, new_order_number):
  	Image.objects.filter(order_number__gte=new_order_number).exclude(pk=self.pk).update(order_number=models.F('order_number') + 1)

  	self.order_number = new_order_number
  	self.save()