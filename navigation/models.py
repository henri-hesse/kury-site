from django.db import models
from django.core.exceptions import ValidationError
from pages.models import Page
from django.core.urlresolvers import reverse

class ItemQuerySet(models.QuerySet):
  def top_level(self):
    return self.filter(parent=None)

  def by_parent(self, parent):
    return self.filter(parent=parent)

  def not_item_or_its_offspring(self, item):
    keys = map(lambda item: item.pk, item.offspring())
    keys.append(item.pk)

    return self.exclude(pk__in=keys)

  def item_and_its_offspring(self, item):
    keys = map(lambda item: item.pk, item.offspring())
    keys.append(item.pk)

    return self.filter(pk__in=keys)

class Item(models.Model):
  LINK_TYPES = (
    ('page', 'Page'),
    ('tailored_page', 'Tailored page'),
    ('url', 'External URL'),
  )

  TAILORED_PAGES = (
    ('base:landing_page', 'Landing page'),
    ('courses:index', 'Courses'),
  )

  parent = models.ForeignKey('self',
    blank = True,
    null = True,
    related_name = 'children',
    verbose_name = 'Parent navigation item',
    help_text = 'This item will be nested inside of the parent item.'
  )

  title = models.CharField(
    max_length = 200,
    help_text = 'Title will be shown on the navigation menu.'
  )

  link_type = models.CharField(
    max_length = 200,
    blank = True,
    null = True,
    choices = LINK_TYPES,
    help_text = 'Where should the user be taken when this item is clicked?'
  )

  page = models.ForeignKey(Page,
    blank = True,
    null = True,
    help_text = 'Select the page that this item links to.',
  )

  tailored_page = models.CharField(
    max_length = 200,
    blank = True,
    null = True,
    choices = TAILORED_PAGES,
    help_text = 'Select the page that this item links to.'
  )

  url = models.URLField(
    blank = True,
    null = True,
    verbose_name = 'URL',
    help_text = 'URL address that this item links to, like "http://example.com/".',
  )

  order_number = models.IntegerField()
  deepness = models.IntegerField()

  objects = ItemQuerySet.as_manager()

  class Meta:
    ordering = ['order_number']

  def __unicode__(self):
    return self.title

  def __init__(self, *args, **kwargs):
    super(Item, self).__init__(*args, **kwargs)

    if self.deepness == None:
      self.refresh_deepness()

  def __setattr__(self, name, value):
    super(Item, self).__setattr__(name, value)

    if name == 'parent':
      self.refresh_deepness()

  def refresh_deepness(self):
    parent = self.parent
    deepness = 0

    while parent is not None:
      parent = parent.parent
      deepness += 1

    self.deepness = deepness

  def clean(self):
    if self.link_type == 'page' and self.page is None:
      raise ValidationError({'page': 'Page cannot be empty.'})

    if self.link_type == 'tailored_page' and self.tailored_page is None:
      raise ValidationError({'tailored_page': 'Page cannot be empty.'})

    if self.link_type == 'url' and (self.url is None or self.url == '' ):
      raise ValidationError({'url': 'URL cannot be empty'})

  def link(self):
    if self.link_type == 'page':
      return self.page.link()

    if self.link_type == 'tailored_page':
      return reverse(self.tailored_page)

    if self.link_type == 'url':
      return self.url

  def tailored_page_label(self):
    iterator = (page[1] for page in Item.TAILORED_PAGES if page[0] == self.tailored_page)
    return next(iterator)

  def offspring(self):
    def recurse(current_items):
      for item in current_items:
        items.append(item)
        recurse(item.children.all())

    items = []
    recurse(self.children.all())

    return items

  def next_sibling(self):
    return Item.objects.by_parent(self.parent).filter(order_number = self.order_number + 1).first()

  def siblings(self):
    return Item.objects.by_parent(self.parent).exclude(pk=self.pk)

  def offspring_count(self):
    return Item.objects.item_and_its_offspring(self).count()

  def last_offspring(self):
    item = self
    child = item.children.last()
    while child is not None:
      item = child
      child = item.children.last()

    return item

  def refresh_offspring_order_numbers(self):
    def recurse(current_items, current_offset):
      for item in current_items:
        current_offset += 1
        item.order_number = self.order_number + current_offset
        item.save()

        recurse(item.children.all(), current_offset)

    recurse(self.children.all(), 0)

  def refresh_later_order_numbers(self):
    later_items = Item.objects.filter(order_number__gte=self.order_number)
    later_items = later_items.not_item_or_its_offspring(self).all()

    offspring_count = self.offspring_count()

    for item in later_items:
      item.order_number += offspring_count
      item.save()

  def detach(self):
    if self.pk is None:
      return

    offspring_count = self.offspring_count()
    later_items = Item.objects.filter(order_number__gte=self.order_number).all()

    for item in later_items:
      item.order_number -= offspring_count
      item.save()

  def attach_before_item(self, item):
    self.detach()

    self.order_number = item.order_number
    self.parent = item.parent
    self.save()

    self.refresh_offspring_order_numbers()
    self.refresh_later_order_numbers()

  def attach_to_parents_end(self):
    self.detach()

    if self.parent is not None:
      self.parent.refresh_from_db()

    last_child = Item.objects.by_parent(self.parent).last()

    if self.parent is None and last_child is None:
      self.order_number = 0

    if self.parent is not None and last_child is None:
      self.order_number = self.parent.order_number + 1

    if last_child is not None:
      self.order_number = last_child.order_number + 1

    self.save()

    self.refresh_offspring_order_numbers()
    self.refresh_later_order_numbers()
