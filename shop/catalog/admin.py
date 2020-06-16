from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Item)
admin.site.register(ItemPhoto)

admin.site.register(GlobalTag)
admin.site.register(LocalTag)
