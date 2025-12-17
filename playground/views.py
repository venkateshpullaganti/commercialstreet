
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Count, Min, Max,Avg,Sum
from django.db.models import Value,F,Func, ExpressionWrapper, DecimalField
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.mail import BadHeaderError, send_mail,mail_admins, EmailMessage
from templated_mail.mail import BaseEmailMessage


from .tasks import notify_customers
from store.models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product
from tags.models import TaggedItem
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
    # products = Product.objects.select_related("collection").all()
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
    # agg = Product.objects.filter(collection_id=3).aggregate(min=Min('unit_price'),max=Max('unit_price'), average=Avg('unit_price'))


    # ## Anotations:
    # products = Product.objects.annotate(is_new=Value(True))
    # products = Product.objects.annotate(new_id=F('id')+1)[:10]
    # for product in products:
    #     print(product.new_id)


    ### Functions
    # customers = Customer.objects.annotate(full_name= Func(F("first_name"),Value(" "),Func("last_name")),function="CONCAT")
    # customers = Customer.objects.annotate(full_nam=Concat("first_name",Value(" "),"last_name"))

    ### Grouping
    # queryset = Customer.objects.annotate(count=Count("order"))


    ### Expression Wrapper
    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField())
    # queryset = Product.objects.annotate(discounted_price=discounted_price)


    ### Annotating Exercise
    # Customers with their last order ID
    # queryset = Customer.objects.annotate(last_order=Max('order__id'))
    # All customers with their order
    # queryset = OrderItem.objects.select_related('order').prefetch_related("order__customer").annotate(customer_id=F("order__customer__id"),placed_order_id=F("order__id"))

    # Collections and count of their products
    # queryset = Collection.objects.annotate(product_count=Count('product__id'))

    # Customers with more than 5 orders
    # queryset = Customer.objects.prefetch_related('order_set').annotate(total_orders=Count("order__id")).filter(total_orders__gte=5)

    # Customers and the total amount they’ve spent
    # queryset = Customer.objects.prefetch_related("order_set","order_set__orderitem_set__product").annotate(amount_spent=Sum(F("order__orderitem__product__unit_price") * F(orderitem__quantity))).order_by("-amount_spent")

    # Top 5 best-selling products and their total sales
    # revenue_contribution = ExpressionWrapper(F("unit_price")* F('total_orders'), output_field=DecimalField())
    # queryset = Product.objects.prefetch_related("orderitem_set").annotate(total_orders=Count(F("orderitem__id"))).annotate(revenue_contribution=revenue_contribution).order_by("-total_orders")[:5]

    ### Querying Generic Relationships

    # Get the tags of a product
    # product_id = 1
    # content_type = ContentType.objects.get_for_model(Product)

    # queryset = TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=product_id)

    ### Custom Manager
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)

    ### Create object
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()

    ### Updating Objects
    # Normal Update all fields
#     collection = Collection(pk=11)
#     collection.title = 'Games'
#     collection.featured_product = Product(pk=1)
#     collection.save()

#    # Update only specific field like below results in data loss of other columns
#     collection = Collection(pk=11)
#     # collection.title will be ''
#     collection.featured_product = Product(pk=1)
#     collection.save()

#     # recomended way
#     collection = Collection.objects.filter(pk=11)    # get data from db
#     collection.featured_product = Product(pk=1)     # update the required fields 
#     collection.save()                               # save 

#     # another way but this will be fragile as the keys featured_product will not be update 
#     Collection.objects.filter(pk=11).update(featured_product=None)

#     # Create a shopping cart with an item
#     cart = Cart()
#     cart.created_at=datetime.now() 
#     cart.save()

#     cartItem = CartItem()
#     cartItem.cart = cart
#     cartItem.product = Product(pk=1)
#     cartItem.save()

#     # Update the quantity of an item in a shopping cart
#     cartItem.quantity = 10
    
#     # Remove a shopping cart with its items
#     cartItem = CartItem(pk=1)
#     cartItem.delete()



    # product_ids = list()
    # for product in products:
    #     product_ids.append(product.id)
    # product_ids=tuple(product_ids)
    # print(len(product_ids))
    # products_orders = OrderItem.objects.filter(product__collection__id=3)
    # print(len(collections))
    # print([products_order.unit_price for products_order in products_orders])

    # Using the Django template to return html with the context object
    # return render(request, "hello.html",{"name":"Jarvis", "products": products, "customers":[], "collections":[], "query_set":[], 'agg':agg}) 



    # Sending email
    # try:
    #     # send_mail("subject", "message", "commercialstreet@gmail.com", ["bob@gmail.com"])
    #     # mail_admins("subject", "message", html_message="html message")

    #     # Email with Attachments 
    #     # message = EmailMessage("subject", "message", "commercialstreet@gmail.com", ["bob@gmail.com"])
    #     # message.attach_file("media/tanjiro.jpg")
    #     # message.send()

    #     #Templated Email
    # message = BaseEmailMessage(template_name="email/hello.html", context={"name":"Tanjiro"})
    # message.send(["tanjiro123@gmail.com"])

        
    # except BadHeaderError as e:
    #     print(e)

    notify_customers.delay("hello world")

    return render(request, "hello.html")