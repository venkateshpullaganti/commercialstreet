from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    search_fields = ['label']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
    