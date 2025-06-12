from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


class InlineTag(GenericTabularInline):
    model = TaggedItem
    extra = 0



class CustomProductAdmin(ProductAdmin):
    inlines = [InlineTag]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


