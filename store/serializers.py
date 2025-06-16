from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    id = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
