from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Count, Min, Max,Avg
from django.db.models import Value,F

from store.models import Collection, Customer, Order, OrderItem, Product
# Create your views here.


def say_hello(request):
    # products = Product.objects.filter(collection__id=3)
    # customers = Customer.objects.filter(email__icontains='com')

    # collections = Collection.objects.filter(featured_product_id__isnull=True)
    # orders = Order.objects.filter(customer__id=1)

    # products: inventory < 10 AND price < 20
    # products = Product.objects.filter(inventory__lte = 10, unit_price__lte = 20 )
    # can be written as 
    # products =  Product.objects.filter(inventory__lte = 10).filter(unit_price__lte = 20)

    # Order items for products in collection 3
    # products = Product.objects.filter(collection_id=3)
    # ids = [product.id for product in list(products)]
    # orders = OrderItem.objects.filter(product_id__in=ids)

    # orders = OrderItem.objects.filter(product__collection__id=3)
    # print(len(list(orders)))
   
   # products: inventory < 10 OR price < 20
    # products =  Product.objects.filter(Q(inventory__lte = 10) | Q(unit_price__lte = 20))
    
    # Products inventory < 10 AND NOT price < 20f
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
    # products = Product.objects.filter(id__in = OrderItem.objects.values('product__id').distinct()).order_by('title')


    ## Selected Related Fields
    products = Product.objects.select_related("collection").all()
    # products = Product.objects.select_related("collection__SomeOtherField").all() -> Will include that someOtherField that is related to the collection, product joins collection joins someOtherField

    # products = Product.objects.prefetch_related("promotions").select_related("collection").all()

    # When 1 - 1 relation we use selected_related
    # When 1-n relation we use prefetch_related

    # Get the last 5 orders with their customer and items (incl product)
    # order_items = OrderItem.objects.select_related('order','product','order__customer').all[:5]
    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # for order in query_set:
    #     print(f"\nOrder ID: {order.id}, Customer: {order.customer.first_name}")
    #     for item in order.orderitem_set.all():
    #         print(f"  - Product: {item.product.title}, Quantity: {item.quantity}, Price: {item.unit_price}")


    ## Aggregations
    # total products
    # agg = Product.objects.aggregate(count=Count('id'), max_price=Max('unit_price'), min_price=Min('unit_price'))

    # Exercise:
    # How many units of product 1 have we sold?
    # agg = OrderItem.objects.select_related("product").filter(product__id=1).aggregate(total=Count('id'))

    # How many orders has customer 1 placed?
    # agg = Order.objects.select_related("customer").filter(customer__id=1).aggregate(customer_1=Count(id))

    # What is the min, max and average price of the products in collection 3?
    agg = Product.objects.filter(collection_id=3).aggregate(min=Min('unit_price'),max=Max('unit_price'), average=Avg('unit_price'))


    ## Anotations:
    products = Product.objects.annotate(is_new=Value(True))
    products = Product.objects.annotate(new_id=F('id')+1)[:10]
    for product in products:
        print(product.new_id)

    # product_ids = list()
    # for product in products:
    #     product_ids.append(product.id)
    # product_ids=tuple(product_ids)
    # print(len(product_ids))
    # products_orders = OrderItem.objects.filter(product__collection__id=3)
    # print(len(collections))
    # print([products_order.unit_price for products_order in products_orders])

    # Using the Django template to return html with the context object
    return render(request, "hello.html",{"name":"Jarvis", "products": products, "customers":[], "collections":[], "query_set":[], 'agg':agg}) 

