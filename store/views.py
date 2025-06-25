
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.db.models.aggregates import Count

from .models import Product,Collection
from .serializers import CollectionSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete(self, request,pk, *args, **kwargs):
        product = get_object_or_404(Product,pk=pk)
        if product.orderitems.count() > 0:
            return Response( {"error":"Product cannot be deleted as it is associated with order item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all() 
    serializer_class = CollectionSerializer

    def get_serializer_context(self ):
        return {'request':self.request}
    
    def delete(self, request,pk, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
        if collection.products.count() > 0:
            return Response( {"error":"collection cannot be deleted as it is associated with product item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductList(ListCreateAPIView):

    #1. attributes
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer


    #2. overriding fns

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}


    # 3. Old approach with APIView inheritance

    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all() # To load the product and collections together
    #     serializer = ProductSerializer(queryset, many=True,context={'request':request})
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # print(serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer


    def delete(self, request,pk, *args, **kwargs):
        product = get_object_or_404(Product,pk=pk)
        if product.orderitems.count() > 0:
            return Response( {"error":"Product cannot be deleted as it is associated with order item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all() 
    serializer_class = CollectionSerializer

    def get_serializer_context(self ):
        return {'request':self.request}
    
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all() 
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete(self, request,pk, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
        if collection.products.count() > 0:
            return Response( {"error":"collection cannot be deleted as it is associated with product item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



# # Create your views here.
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all() # To load the product and collections together
#         serializer = ProductSerializer(queryset, many=True,context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
#     product = get_object_or_404(Product,pk=id)

#     if request.method == 'GET':
#         serializer= ProductSerializer(product, context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response( {"error":"Product cannot be deleted as it is associated with order item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all() 
#         serializer = CollectionSerializer(queryset, many=True,context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
     



# @api_view(['GET','PUT','DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
#     if request.method == 'GET':
#         serializer= CollectionSerializer(collection, context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response( {"error":"collection cannot be deleted as it is associated with product item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

