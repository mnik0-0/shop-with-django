from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Item)
admin.site.register(models.ItemPhoto)

admin.site.register(models.GlobalTag)
admin.site.register(models.LocalTag)
