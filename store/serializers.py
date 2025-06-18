from decimal import Decimal
from rest_framework import serializers

from store.models import Collection, Product


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)



class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    id = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # renamed field
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')  # Custom field

    # Serializing Relations

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
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name='collection-detail' # Create a api with name collection-detail and the lookup field is pk in the url definition
    )
    # {
    #     "title": "7up Diet, 355 Ml",
    #     "id": 648,
    #     "unit_price": 79.07,
    #     "price": 79.07,
    #     "price_with_tax": 86.977,
    #     "collection": "http://127.0.0.1:8000/store/collection/5/"
    # },

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)
