from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all() # To load the product and collections together
    serializer = ProductSerializer(queryset, many=True,context={'request':request})
    return Response(serializer.data)


@api_view()
def product_detail(request,id):
    product = get_object_or_404(Product,pk=id)
    serializer= ProductSerializer(product, context={'request':request})

    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    return Response('ok')