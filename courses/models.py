from __future__ import unicode_literals
from django.db import models
import markdown
from django.utils import timezone

class CourseQuerySet(models.QuerySet):
  def visible(self):
    return self.filter(events__datetime__gte=timezone.now()).distinct()

class Course(models.Model):
  title = models.CharField(
  	max_length = 200,
  	verbose_name = 'Short title',
  	help_text = 'Short title name for the course. Do not add any specific dates here.'
  )
  description = models.TextField(
  	verbose_name = 'Longer description',
  	help_text = 'Complete description of the course. May contain special markup. Do not add any specific dates here.'
  )
  image = models.ImageField(
  	upload_to = 'courses/',
  	verbose_name = 'General image of the course',
  	help_text = 'Pick up a image file from your computer. Image should be big enough so that it wont get scaled up by the system.'
  )

  def __unicode__(self):
    return self.title

  objects = CourseQuerySet.as_manager()

  def description_html(self):
    return markdown.markdown(self.description, extensions=['markdown.extensions.nl2br'])

  def visible_events(self):
    return filter(lambda event: event.datetime >= timezone.now(), self.events.all())

class CourseEvent(models.Model):
  course = models.ForeignKey(Course,
    related_name = 'events',
    verbose_name = 'Course',
    help_text = 'Course that this event belongs to.'
  )
  datetime = models.DateTimeField(
  	verbose_name = 'Date & time',
  	help_text = 'When this event is planned to happen',
  )
  store_link = models.URLField(
  	verbose_name = 'Link to the web store',
  	help_text = 'Provide complete URL to the web store.'
  )

  def __unicode__(self):
  	return self.course + ': ' + self.datetime

  class Meta:
    ordering = ['datetime']