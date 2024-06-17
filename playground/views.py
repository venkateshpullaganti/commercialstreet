from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q,F

from store.models import Collection, Customer, Order, OrderItem, Product
# Create your views here.


def say_hello(request):
    # products = Product.objects.filter(collection__id=3)
    customers = Customer.objects.filter(email__icontains='com')

    # collections = Collection.objects.filter(featured_product_id__isnull=True)
    # orders = Order.objects.filter(customer__id=1)

    # products: inventory < 10 AND price < 20
    # products = Product.objects.filter(inventory__lte = 10, unit_price__lte = 20 )
    # can be written as 
    # products =  Product.objects.filter(inventory__lte = 10).filter(unit_price__lte = 20)
   
   # products: inventory < 10 OR price < 20
    # products =  Product.objects.filter(Q(inventory__lte = 10) | Q(unit_price__lte = 20))
    
    # Products inventory < 10 AND NOT price < 20
    # products =  Product.objects.filter(Q(inventory__lte = 10) | ~Q(unit_price__lte = 20))

    # Products inventory =  price
    # products = Product.objects.filter(inventory=F('unit_price'))
    # products = Product.objects.filter(inventory=F('collection__id'))

    # Order by title Ascending order
    # products = Product.objects.filter(inventory=F('collection__id')).order_by("title")

    # Earliset & Latest
    # product = Product.objects.filter(inventory=F('collection__id')).earliest("title")
    # print(product.title)


    # Limiting / paginating
    # products = Product.objects.all()[:20] # First 20 objects

    # Querying only some fields
    # products = Product.objects.values_list('id', 'title', 'collection__title')

    # Select products that have been ordered and sort them by title
    products = Product.objects.filter(id__in = OrderItem.objects.values('product__id').distinct()).order_by('title')


    # product_ids = list()
    # for product in products:
    #     product_ids.append(product.id)
    # product_ids=tuple(product_ids)
    # print(len(product_ids))
    # products_orders = OrderItem.objects.filter(product__collection__id=3)
    # print(len(collections))
    # print([products_order.unit_price for products_order in products_orders])

    # Using the Django template to return html with the context object
    return render(request, "hello.html",{"name":"Jarvis", "products": list(products), "customers":list(customers)}) 