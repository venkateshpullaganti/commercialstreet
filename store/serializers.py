import datetime
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from store.signals import order_created


from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title','products_count']

    products_count = serializers.IntegerField(read_only=True)

    # def count_products(self, collection:Collection):
    #     return collection.aggregate.count()

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price'] 


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title','description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # fields = '__all__' # bad practice - lazy dev

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')  # Custom field

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price'] 
    
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cartItem:CartItem):
        return cartItem.quantity * cartItem.product.unit_price


# Add new item to the cart
# 1. Add post cartitem serializer & reurn based on the request type
# 2. Pass id in the serializer context
# 3. Override the save method to handle save and update

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Not Product found with given ID.')
        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):

   
    class Meta:
        model = Cart
        fields = ['id','items','total_price']

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone',"birth_date" ,"membership"]    


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product','quantity','unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields =  ['id', 'payment_status', 'customer', 'placed_at', 'items']

class CreateOrderSerialzer(serializers.Serializer):
    cart_id = serializers.UUIDField()


    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("Cart doesn't exist")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("Cart is empty")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity= item.quantity
                ) for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.get(id=cart_id).delete()
            
            order_created.send_robust(self.__class__, order=order)
            return order

class UpdateOrderSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Order
        fields =  ['payment_status']


    # products = serializers.SerializerMethodField(method_name='cartitems')

    # def cartitems(self, cart:Cart):
    #     return cart.items.id

    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.last_update = datetime.time()
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do no match')
    #     return data


    # -------------------------------------------------------------------

    # plain serialization notation

    # title = serializers.CharField(max_length=255)
    # id = serializers.IntegerField()
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # renamed field

    # -------------------------------------------------------------------

    # Serializing Relations : 4 ways

    # 1. Primary Key
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )

    #     {
    #     "title": "7up Diet, 355 Ml",
    #     "id": 648,
    #     "unit_price": 79.07,
    #     "price": 79.07,
    #     "price_with_tax": 86.977,
    #     "collection": 5
    # }

    # 2. String
    # collection = serializers.StringRelatedField()  # This will query the each collection separately for title if we don't load the products with selected_related('collection) 
    # {
    #     "title": "7up Diet, 355 Ml",
    #     "id": 648,
    #     "unit_price": 79.07,
    #     "price": 79.07,
    #     "price_with_tax": 86.977,
    #     "collection": "Stationary"
    # }


    # 3. Nested Object
    # collection = CollectionSerializer()
    #     {
    #     "title": "7up Diet, 355 Ml",
    #     "id": 648,
    #     "unit_price": 79.07,
    #     "price": 79.07,
    #     "price_with_tax": 86.977,
    #     "collection": {
    #         "id": 5,
    #         "title": "Stationary"
    #     }
    # }

    # 4. Hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail' # Create a api with name collection-detail and the lookup field is pk in the url definition
    # )
    # {
    #     "title": "7up Diet, 355 Ml",
    #     "id": 648,
    #     "unit_price": 79.07,
    #     "price": 79.07,
    #     "price_with_tax": 86.977,
    #     "collection": "http://127.0.0.1:8000/store/collection/5/"
    # },
