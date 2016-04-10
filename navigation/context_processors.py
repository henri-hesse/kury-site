from .models import *

def top_level_items(request):
  return {'top_level_items': Item.objects.top_level()}
