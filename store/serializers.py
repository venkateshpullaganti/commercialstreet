import datetime
from decimal import Decimal
from rest_framework import serializers

from store.models import Collection, Product


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title','products_count']

    products_count = serializers.IntegerField(read_only=True)

    # def count_products(self, collection:Collection):
    #     return collection.aggregate.count()



class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title','description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # fields = '__all__' # bad practice - lazy dev

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')  # Custom field

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
    

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

    