from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify
import markdown

class Page(models.Model):
  title = models.CharField(max_length=200)
  content = models.TextField()

  def __unicode__(self):
    return self.title

  def link(self):
    return reverse('pages:show_page', kwargs={'pk': self.pk, 'slug': slugify(self.title)})

  def content_html(self):
    return markdown.markdown(self.content, extensions=['markdown.extensions.nl2br'])