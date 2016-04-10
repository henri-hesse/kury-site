from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import *
from .forms import *

class ItemTests(TestCase):
  def create_some_items(self):
    self.i1 = Item.objects.create(order_number=0, title='i1')
    self.i11 = Item.objects.create(parent=self.i1, order_number=1, title='i11')
    self.i12 = Item.objects.create(parent=self.i1, order_number=2, title='i12')
    self.i121 = Item.objects.create(parent=self.i12, order_number=3, title='i121')
    self.i2 = Item.objects.create(order_number=4, title='i2')

  def test_clean(self):
    item = Item(order_number=0, title='test')
    page = Page.objects.create(title='test')

    item.link_type = 'page'
    with self.assertRaises(ValidationError) as cm:
      item.full_clean()

    errors = cm.exception.message_dict
    self.assertEqual(1, len(errors))
    self.assertEqual(True, 'page' in errors)

    item.link_type = 'tailored_page'
    with self.assertRaises(ValidationError) as cm:
      item.full_clean()

    errors = cm.exception.message_dict
    self.assertEqual(1, len(errors))
    self.assertEqual(True, 'tailored_page' in errors)

    item.link_type = 'url'
    with self.assertRaises(ValidationError) as cm:
      item.full_clean()

    errors = cm.exception.message_dict
    self.assertEqual(1, len(errors))
    self.assertEqual(True, 'url' in errors)

    item.url = ''
    with self.assertRaises(ValidationError) as cm:
      item.full_clean()

    errors = cm.exception.message_dict
    self.assertEqual(1, len(errors))
    self.assertEqual(True, 'url' in errors)

  def test_tailored_page_label(self):
    item = Item(tailored_page=Item.TAILORED_PAGES[0][0])
    self.assertEqual(Item.TAILORED_PAGES[0][1], item.tailored_page_label())

  def test_by_parent(self):
    self.create_some_items()

    items = Item.objects.by_parent(None).all()
    self.assertEqual(self.i1, items[0])
    self.assertEqual(self.i2, items[1])

  def test_not_item_or_its_offspring(self):
    self.create_some_items()

    items = Item.objects.not_item_or_its_offspring(self.i12)

    self.assertEqual(self.i1, items[0])
    self.assertEqual(self.i11, items[1])
    self.assertEqual(self.i2, items[2])

  def test_item_and_its_offspring(self):
    self.create_some_items()
    items = Item.objects.item_and_its_offspring(self.i12)

    self.assertEqual(2, len(items))
    self.assertEqual(self.i12, items[0])
    self.assertEqual(self.i121, items[1])

  def test_refresh_deepnees(self):
    self.create_some_items()

    new_item = Item(parent=self.i11)
    self.assertEqual(2, new_item.deepness)

    new_item.parent = None
    self.assertEqual(0, new_item.deepness)

  def test_next_sibling(self):
    self.create_some_items()

    self.assertEqual(self.i12, self.i11.next_sibling())

  def test_top_level(self):
    self.create_some_items()
    items = Item.objects.top_level()

    self.assertEqual(2, len(items))
    self.assertEqual(self.i1, items[0])
    self.assertEqual(self.i2, items[1])

  def test_offspring(self):
    self.create_some_items()
    items = self.i1.offspring()

    self.assertEqual(3, len(items))
    self.assertEqual(self.i11, items[0])
    self.assertEqual(self.i12, items[1])
    self.assertEqual(self.i121, items[2])

  def test_offspring_count(self):
    self.create_some_items()
    self.assertEqual(2, self.i12.offspring_count())

  def test_siblings(self):
    self.create_some_items()
    items = self.i12.siblings()

    self.assertEqual(1, len(items))
    self.assertEqual(self.i11, items[0])

  def test_detach(self):
    self.create_some_items()

    self.i12.detach()

    self.i121.refresh_from_db()
    self.i2.refresh_from_db()

    self.assertEqual(2, self.i2.order_number)

  def test_last_offspring(self):
    self.create_some_items()

    self.assertEqual(self.i121, self.i1.last_offspring())

  def test_attach_before_item(self):
    self.create_some_items()

    self.i12.attach_before_item(self.i1)

    self.i1.refresh_from_db()
    self.i11.refresh_from_db()
    self.i12.refresh_from_db()
    self.i121.refresh_from_db()
    self.i2.refresh_from_db()

    self.assertEqual(0, self.i12.order_number)
    self.assertEqual(1, self.i121.order_number)
    self.assertEqual(2, self.i1.order_number)
    self.assertEqual(3, self.i11.order_number)
    self.assertEqual(4, self.i2.order_number)

    self.assertEqual(None, self.i12.parent)

  def test_attach_to_parents_end_when_empty_db(self):
    new_item = Item(parent=None)
    new_item.attach_to_parents_end()

    self.assertEqual(0, new_item.order_number)

  def test_attach_to_parents_end_when_empty_parent(self):
    self.create_some_items()

    new_item = Item(parent=self.i121)
    new_item.attach_to_parents_end()

    self.i2.refresh_from_db()

    self.assertEqual(4, new_item.order_number)
    self.assertEqual(5, self.i2.order_number)

  def test_attach_to_parents_end_when_not_empty_parent(self):
    self.create_some_items()

    new_item = Item(parent=None)
    new_item.attach_to_parents_end()

    self.assertEqual(5, new_item.order_number)

class ItemFormTests(TestCase):
  def create_some_items(self):
    self.i1 = Item.objects.create(title='i1', order_number=0)
    self.i11 = Item.objects.create(title='i11', parent=self.i1, order_number=1)
    self.i12 = Item.objects.create(title='i12', parent=self.i1, order_number=2)
    self.i121 = Item.objects.create(title='i121', parent=self.i12, order_number=3)
    self.i2 = Item.objects.create(title='i2', order_number=4)

  def test_fields_with_instance(self):
    self.create_some_items()
    form = ItemForm(instance=self.i12)

    self.assertEqual(True, 'title' in form.fields)

    choices = list(form.fields['parent'].choices)

    self.assertEqual('', choices[0][0])
    self.assertEqual(self.i1.pk, choices[1][0])
    self.assertEqual(self.i11.pk, choices[2][0])
    self.assertEqual(self.i2.pk, choices[3][0])

    self.assertEqual('Top-level', choices[0][1])
    self.assertEqual(self.i1.title, choices[1][1])
    self.assertEqual(self.i11.title, choices[2][1])
    self.assertEqual(self.i2.title, choices[3][1])

    choices = list(form.fields['placement'].choices)

    self.assertEqual(self.i11.pk, choices[0][0])
    self.assertEqual('end', choices[1][0])

    self.assertEqual('Before i11', choices[0][1])
    self.assertEqual('To the end', choices[1][1])

    self.assertEqual('end', form.initial['placement'])

  def test_fields_with_data_and_instance(self):
    self.create_some_items()

    form = ItemForm({'parent': self.i2.pk}, instance=self.i12)

    choices = list(form.fields['placement'].choices)

    self.assertEqual('end', choices[0][0])
    self.assertEqual('To the end', choices[0][1])

    self.assertEqual('end', form.initial['placement'])

  def test_save_with_existing_instance_to_parents_end(self):
    self.create_some_items()

    form = ItemForm({'title': 'i12', 'parent': self.i2.pk, 'placement': 'end'}, instance=self.i12)
    self.assertEqual(True, form.is_valid())

    form.save()

    self.i1.refresh_from_db()
    self.i11.refresh_from_db()
    self.i12.refresh_from_db()
    self.i121.refresh_from_db()
    self.i2.refresh_from_db()

    self.assertEqual(0, self.i1.order_number)
    self.assertEqual(1, self.i11.order_number)
    self.assertEqual(2, self.i2.order_number)
    self.assertEqual(3, self.i12.order_number)
    self.assertEqual(4, self.i121.order_number)

  def test_save_with_existing_instance_to_before_item(self):
    self.create_some_items()

    form = ItemForm({
      'title': 'i12',
      'parent': self.i1.pk,
      'placement': self.i11.pk
    }, instance=self.i12)

    self.assertEqual(True, form.is_valid())

    form.save()

    self.i1.refresh_from_db()
    self.i11.refresh_from_db()
    self.i12.refresh_from_db()
    self.i121.refresh_from_db()
    self.i2.refresh_from_db()

    self.assertEqual(0, self.i1.order_number)
    self.assertEqual(1, self.i12.order_number)
    self.assertEqual(2, self.i121.order_number)
    self.assertEqual(3, self.i11.order_number)
    self.assertEqual(4, self.i2.order_number)
