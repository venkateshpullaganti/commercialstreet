from django.contrib import admin
from django.db.models import Count
from django.utils.html import urlencode,format_html
from django.urls import reverse

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','inverntory_status',"collection_title"]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inverntory_status(self,product):
        if product.inventory < 10:
            return "Low"
        return "OK"
    
    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','email']
    list_editable = ['membership']
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']
    list_per_page = 10
    ordering = ['title']

    @admin.display(ordering='product_count')
    def product_count(self,collection):
        url = (reverse('admin:store_product_changelist')
               + '?' 
               + urlencode({
                   'collection__id' : str(collection.id)
               })
               )
        return format_html('<a href="{}">{}</a>', url,collection.product_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer','placed_at','payment_status']
    list_select_related = ['customer']
    ordering = ['customer']

