from django import forms
from .models import *

class ItemForm(forms.ModelForm):

  class Meta:
    model = Item
    fields = ('title', 'parent', 'link_type', 'page', 'tailored_page', 'url')
    widgets = {
      'title': forms.TextInput(
        attrs = { 'class': 'form-control' }
      ),
      'parent': forms.Select(
        attrs = {
          'class': 'form-control',
          'data-kury-refresh-form': ''
        }
      ),
      'link_type': forms.Select(
        attrs = {
          'class': 'form-control',
          'data-kury-refresh-form': ''
        }
      ),
      'page': forms.Select(
        attrs = { 'class': 'form-control' }
      ),
      'tailored_page': forms.Select(
        attrs = { 'class': 'form-control' }
      ),
      'url': forms.TextInput(
        attrs = { 'class': 'form-control' }
      ),
    }

  def __init__(self, *args, **kwargs):
    self.placement_field_initial(kwargs)

    super(ItemForm, self).__init__(*args, **kwargs)

    self.parent_field()
    self.placement_field()

  def save(self, *args, **kwargs):
    placement = self.cleaned_data['placement']

    if placement == 'end':
      self.instance.attach_to_parents_end()
    else:
      item = Item.objects.get(pk=placement)
      self.instance.attach_before_item(item)

    super(ItemForm, self).save(*args, **kwargs)

  def parent_field(self):
    queryset = self.fields['parent'].queryset
    if self.instance.pk is not None:
      self.fields['parent'].queryset = queryset.not_item_or_its_offspring(self.instance)

    self.fields['parent'].empty_label = 'Top-level'

  def placement_field(self):
    if 'parent' in self.data:
      if self.data['parent'] != '':
        self.instance.parent = Item.objects.get(pk=self.data['parent'])
      else:
        self.instance.parent = None

    choices = map(
      lambda item: (item.pk, 'Before ' + item.title),
      self.instance.siblings()
    )
    choices.append(('end', 'To the end'))

    self.fields['placement'] = forms.ChoiceField(
      choices = choices,
      help_text = 'Select a place inside the parent item.',
      widget = forms.Select(
        attrs = { 'class': 'form-control' }
      )
    )

  def placement_field_initial(self, kwargs):
    if kwargs.get('instance', None) is None: return

    kwargs['initial'] = kwargs.get('initial', {})
    next_sibling = kwargs['instance'].next_sibling()

    if next_sibling is not None:
      kwargs['initial']['placement'] = next_sibling.pk
    else:
      kwargs['initial']['placement'] = 'end'


  ''' This was my old idea of having only one placement dropdown to handle sorting & parent item
      all in one go, but I desided to get rid of it. It was getting so complicated. - Hesse

  def __init__(self, *args, **kwargs):
    kwargs['instance'] =  kwargs.get('instance', None)

    if kwargs['instance'] is not None:
      kwargs['initial'] = kwargs.get('initial', {})

      next_sibling = kwargs['instance'].next_sibling()
      kwargs['initial']['placement'] = self.build_placement_choices_for_item(next_sibling)[0][0]

    super(ItemForm, self).__init__(*args, **kwargs)

    self.build_placement_field()

  def save(self, *args, **kwargs):
    placement = self.cleaned_data['placement'].split('_')
    method = placement[0]
    item = Item.objects.get(pk=placement[1])

    changed_items = self.instance.detach()

    if method == 'before':
      changed_items += self.instance.attach_before_item(item)
    elif method == 'inside':
      self.instance.attach_inside_empty_item(item)
    elif method == 'endof':
      self.instance.attach_to_children_end(item.parent)

    for item in changed_items:
      item.save()

    super(ItemForm, self).save(*args, **kwargs)

  def build_placement_field(self):
    pks = []
    if self.instance.pk is not None:
      pks = Item.map_pks(self.instance.offspring())
      pks.append(self.instance.pk)

    choices = []
    def recurse(current_items, deepness):
      for item in current_items.without_pks(pks):
        choices.extend( self.build_placement_choices_for_item(item, deepness) )
        recurse(item.children, deepness + 1)

    recurse(Item.objects.top_level(), 0)

    self.fields['placement'] = forms.ChoiceField(
      label = 'Placement',
      choices = choices
    )

  def build_placement_choices_for_item(self, item, deepness=0):
    value = 'before_' + str(item.pk)
    label = '>' * deepness + ' Before ' + item.title
    choices = [ (value, label) ]

    if not item.has_children():
      value = 'inside_' + str(item.pk)
      label = '>' * (deepness + 1) + ' Inside ' + item.title
      choices.append( (value, label) )

    if item.is_last_child():
      value = 'endof_'
      label = '>' * deepness + ' End of '

      if item.parent is not None:
        label += item.parent.title
        value += str(item.parent.id)
      else:
        label += 'top-level'
        value += 'toplevel'

      choices.append( (value, label) )

    return choices

  class Meta:
    model = Item
    fields = ('title',)
  '''

class PageForm(forms.ModelForm):

  class Meta:
    model = Page
    fields = ('title', 'content')
    widgets = {
      'title': forms.TextInput(
        attrs = { 'class': 'form-control' }
      ),
      'content': forms.Textarea(
        attrs = { 'class': 'form-control' }
      ),
    }
