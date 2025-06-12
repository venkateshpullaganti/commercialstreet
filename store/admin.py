from django.contrib import admin
from django.db.models import Count
from django.utils.html import urlencode,format_html
from django.urls import reverse
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset):
        if(self.value() == '<10'):
            return queryset.filter(inventory__lt=10)
        return queryset


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={
        "slug":['title']
    }
    autocomplete_fields = ['collection']
    actions=['clear_inventory']
    list_display = ['title','unit_price','inverntory_status',"collection_title"]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update',InventoryFilter]
    search_fields = ['title__istartswith']

    @admin.display(ordering='inventory')
    def inverntory_status(self,product):
        if product.inventory < 10:
            return "Low"
        return "OK"
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        count = queryset.update(inventory=0)
        self.message_user(
            request, 
            f'{count} products updated successfully')
        

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','email','total_orders']
    list_editable = ['membership']
    list_per_page = 10
    search_fields=['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='order')
    def total_orders(self, customer):
        url = reverse('admin:store_order_changelist') + "?" + urlencode({
            'customer__id':customer.id
        })
        return format_html('<a href={}>{}</a>',url , customer.total_orders)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_orders=Count('order'))




@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']
    list_per_page = 10
    ordering = ['title']
    search_fields = ['title']

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

class OrderInlineItem(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'customer','placed_at','payment_status']
    list_select_related = ['customer']
    inlines= [OrderInlineItem]
    ordering = ['customer']

