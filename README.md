# Django

### Creating Django Application

- Install Django
    
    ```python
    pipenv install django
    ```
    
    - cd into the folder
- activates the virtual environment
    
    ```python
    pipenv shell
    ```
    
- Create a Django project
    
    ```python
    django admin startproject <project_name> . # adding . at end creates the project directly
    ```
    
- run project
    
    ```python
    python manage.py runserver
    ```
    
- Add the python interpreter to the vscode
    - run `pipenv --venv` in the project folder and copy the path
        - past the path in the vscode select interpreter command → paste the above path add `/bin/python` to the copied path

### Adding an API

- 1. Write a view handler  in `playground/views.py`
    
    ```jsx
    from django.shortcuts import render
    from django.http import HttpResponse
    # Create your views here.
    
    def calculate():
        y = 4
        x = 3
        return x
    
    def say_hello(request):
        x = calculate()
        print(x)
        
        # Using the Django template to return html with the context object
        return render(request, "hello.html",{"name":"Jarvis"}) 
    ```
    
- 2.Add it to it’s app urls for endpoint `playground/urls.py`
    
    ```jsx
    from django.urls import path
    from . import views
    
    urlpatterns = [
        path("hello/", views.say_hello)
    ]
    ```
    
- 3.Include it in the main app’s urls `commercialstreet/urls`
    
    ```jsx
    """
    URL configuration for commercialstreet project.
    
    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/5.0/topics/http/urls/
    Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    from django.contrib import admin
    from django.urls import include, path
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('playground/', include('playground.urls'))
    ]
    
    ```
    
- 4.Now the api is available at the endpoint `playground/hello/`
- Notes
    1. Always add the `/` at the end of the end point
    2. Create a path with `path` from   `from django.urls import path`
    3. To include all the apis from an app, we need to do `path(<app_prefix>, include(<app.urls>))` 
    

### Adding Models

1. Create a class with inherited models.Model
2. Add different types of the fields based on the requirement
3. There are default value, max, min, choices, make it null, default date etc based on the field
4. For relations we just need to define it at one of the model and the rest will be take care by the django for creating the other side of the relation 
    - While creating the relation it is important to handle when the any one of the model is deleted
        
        ```python
        customer = models.ForeignKey(to=Customer, on_delete = models.PROTECT)
        ```
        
5. For generic models 
    
    ```python
    from django.db import models
    
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.contenttypes.fields import GenericForeignKey
    
    class Tag(models.Model):
        label = models.CharField(max_length=255)
        
        
    class TaggedItem(models.Model):
        tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
        # Generic Model relation
        # What type of the content needs to be created
        # Type : (product, video, blog)
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveIntegerField() # the id of the object/model 
        content_object = GenericForeignKey()     # Actual object/model that a tag is applied on 
    ```
    

### Migrations

1. Add a field / models
2. Create Migrations:  `python [manage.py](http://manage.py) makemigrations` 
3. Apply Migrations: `python [manage.py](http://manage.py) migrate`

### ❗ Revert Migration:

1. `python [manage.py](http://manage.py) migrate store 0004`  → `store 0004` is the migration that you want to move to 
    1. Check the migrations table to ensure. The migrations after store 0004 must have been deleted in the db
2. revert all the changes in the code and delete the migration files
    1. Using git to revert the code is much easier than removing all the changes manually 

Notes:

1. When renamed migration file, need to update dependencies in the next file

### Connecting Databases

1. Select the database that we want to use
2. Install database : Ex: SQL
3. While installing give a password &/ user name [default is root for SQL]
4. Install the client for that db. For sql it is sqlclient `pipenv install sqlclient`
    1. This sometimes causes error. Make sure to check below
        1. Python version
        2. SQL installed version
        3. sqlclient version if not supported go back to previous versions
        4. Try installing out of the virtual env system wide
5. After installing successfully db & client, we need to connect to the db server and create a database `commercialstreet`
    1. For connecting to database we can use the dbweaver community version or some other tools
6. In settings file under the database give below settings
    
    ```python
    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # your database
            'NAME': 'commercialstreet', # name of the db
            'HOST': 'localhost',  # where the db is running
            'USER': 'root',       # user name
            'PASSWORD': 'admin123'# user password
        }
    }
    
    ```
    
7. Now first apply the migrations and check in the db whether all the tables are created 
8. Now load the sample data into the db tables
    1. We can use mockaroo to generate dummy data

### Django ORM / Retrieving Objects

- Abstraction over the sql/db queries
- Each model represents a table
- Each model has object handler
    
    ```python
    from store.models import Product
    
    Product.objects   # object handler
    	query_set = Product.objects.all().      
    	# different methods ex: 
    	   # all -> gets all the products in the table. 
    		 # it return query set where we can further add queries/fns.
    		 # this query set is lazy. executes only when we are using like
    		 # list(query_set), accessing object or slicing etc
    		 # for product in query_set:
    		 #.      prin(product)			
    ```
    
    - We can chain other methods for the query set like `query_set.filter()` etc.
    - Some other methods like `Product.objects.count` / `Product.objects.get(pk=1)` (primary_key)  will return the value itself because it is a constant value
- When the object is not found in the db, it throws the DoesNotExist exception
    - To handle this either wrap the code in the try catch and handle the exception or
    - use `filter()` and then `first()` / `last()` methods. this will return none if object not found
- Query_set extended
    - in Querying we can use multiple methods such as
        
        ```python
        Product.objects.filter(product_price__lte=20) # Filtering price less than/equal to 20
        # similarly there is gte, range=tuple(), in, contains, startswith, istartswith(case Insensitive), iendswith, etc
        
        OrderItems.objects.filter(product_collection__id=3) # OrderItems for Products that are in Collection 3 
        ```
        
- Lookup types and related objects
    
    ```python
    OrderItems.objects.filter(product_collection__id=3) # OrderItems for Products that are in Collection 3
    		# In products table -> collection -> id (we can use any field that is present in the collection table
    		# Also further apply operations on it using the lookup fields : product_collection__id__range=(1,2,3) 
    ```
    
    ```python
        # Select products that have been ordered and sort them by title
        products = Product.objects.filter(id__in = OrderItem.objects.values('product__id').distinct()).order_by('title')
    ```
    
    Example Lookups: https://docs.djangoproject.com/en/5.0/ref/models/querysets/
    
    - let
    - gte
    - range
    - in
    - contains, etc.
    - Complex Conditions using Q object:
        
        AND
        
        ```python
        
            # products: inventory < 10 AND price < 20
        	   products = Product.objects.filter(inventory__lte = 10, unit_price__lte = 20 )
            # can be written as 
            products = Product.objects.filter(inventory__lte = 10).filter(unit_price__lte = 20)
        ```
        
        OR
        
        - We can use Q object to filter using the or (`|`) operator
            
            ```python
            from django.models.db import Q
            
              # products: inventory < 10 OR price < 20
              products =  Product.objects.filter(Q(inventory__lte = 10) | Q(unit_price__lte = 20))
                
              # Products inventory < 10 AND NOT price < 20
              products =  Product.objects.filter(Q(inventory__lte = 10) | **~**Q(unit_price__lte = 20))
            ```
            
    - Reference Fields using F Object :
        
        ```python
            # Products inventory =  price
            products = Product.objects.filter(inventory=F('unit_price'))
            
            
            # Products inventory =  products collection id, the collection is in another table 
            products = Product.objects.filter(inventory=F('collection__id'))
        ```
        
    - Order by
        
        ```python
        # Order by title Ascending order
        products = Product.objects.filter(inventory=F('collection__id')).order_by("title")
        
        # Order by title Descending order
        products = Product.objects.filter(inventory=F('collection__id')).order_by("-title")
        
        products = Product.objects.filter(inventory=F('collection__id')).earliest("title") # only first one
        products = Product.objects.filter(inventory=F('collection__id')).latest("title")   # only last one
        ```
        
    - Limiting
        
        ```python
          # Limiting / paginating
          products = Product.objects.all()[:20] # First 20 objects
        ```
        
    - Querying the related objects: `select_related` & `prefetch_related`
        - To query the related objects, like product’s collection
            
            ```python
            
                ## Selected Related Fields
                # products = Product.objects.select_related("collection").all()
                # products = Product.objects.select_related("collection__SomeOtherField").all() -> Will include that someOtherField that is related to the collection, product joins collection joins someOtherField
            
                products = Product.objects.prefetch_related("promotions").select_related("collection").all()
            
                # When 1 - 1 relation we use selected_related
                # When 1-n relation we use prefetch_related
            
            ```
            
            - Practice
                
                ```python
                    # Get the last 5 orders with their customer and items (incl product)
                    # order_items = OrderItem.objects.select_related('order','product','order__customer').all[:5]
                    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] # orderitem is the reverse foreign relation that django created in order table for orderItem
                
                    for order in query_set:
                        print(f"\nOrder ID: {order.id}, Customer: {order.customer.first_name}")
                        for item in order.orderitem_set.all():
                            print(f"  - Product: {item.product.title}, Quantity: {item.quantity}, Price: {item.unit_price}")
                
                ```
                
    - Only and defer
        
        `only` : Used to query only certain fields in the products. It returns the instances of the product. but the values returns the objects
        
        Caution: If you are accessing any not queried field in the product instances, then it will run the query on each instance again to get that fields
        
        ```python
        products = Product.objects.only('id', 'title')
        
        # While rendering if you access 
        product.unit_price -> this will again run query for unit_price on each product
        
        ```
        
        `defer` :  It is used to exclude some fields in the query. It is opposite for `only` 
        
        ```python
        products = Product.objects.defet("description") 
        # Returns the product instances without description. 
        # But in the next lines somewhere if you access the description on the product field then it will run the query for all the products for description separately 
        ```
        
    - Aggregations
        
        ```python
            from django.db.models.aggregates import Count, Min, Max,Avg
            
            ## Aggregations
            # performing further calculations on the entries in the table
            
            # agg = Product.objects.aggregate(count=Count('id'), max_price=Max('unit_price'), min_price=Min('unit_price'))
        
            # Exercise:
            # How many units of product 1 have we sold?
            # agg = OrderItem.objects.select_related("product").filter(product__id=1).aggregate(total=Count('id'))
        
            # How many orders has customer 1 placed?
            # agg = Order.objects.select_related("customer").filter(customer__id=1).aggregate(customer_1=Count(id))
        
            # What is the min, max and average price of the products in collection 3?
            agg = Product.objects.filter(collection_id=3).aggregate(min=Min('unit_price'),max=Max('unit_price'), average=Avg('unit_price'))
        
        ```
        

### Keyboard shortcuts

1. Search keyword: `cmd+t` 
2.  Go to any symbol in current file:   `cmd+shift+o`


[Full Notes Link](https://www.notion.so/venkyp/Django-b9b984702c4542348cbd6e5f14a2bcde)