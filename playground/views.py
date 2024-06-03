from django.shortcuts import render
from django.http import HttpResponse

from store.models import Collection, Customer, Order, OrderItem, Product
# Create your views here.


def say_hello(request):
    products = Product.objects.filter(collection__id=3)
    customers = Customer.objects.filter(email__icontains='com')
    collections = Collection.objects.filter(featured_product_id__isnull=True)
    orders = Order.objects.filter(customer__id=1)
    product_ids = list()
    for product in products:
        product_ids.append(product.id)
    product_ids=tuple(product_ids)
    print(len(product_ids))
    products_orders = OrderItem.objects.filter(product__collection__id=3)
    # print(len(collections))
    print([products_order.unit_price for products_order in products_orders])

    # Using the Django template to return html with the context object
    return render(request, "hello.html",{"name":"Jarvis", "products": list(products), "customers":list(customers)}) 