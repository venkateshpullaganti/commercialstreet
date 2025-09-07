from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin,DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.pagination import PageNumberPagination

from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewHistoryPermission


from .pagination import DefaultPagination
from .filters import ProductFilterSet
from .models import Cart, CartItem, Customer, Order, OrderItem, Product,Collection, ProductImage, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerialzer, CustomerSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, OrderSerializer, UpdateOrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    pagination_class = DefaultPagination
    search_fields = ['title','description']
    ordering_filelds = ['unit_price','last_update']

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('images').all()
        collection_id = self.request.query_params.get("collection_id")
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)

        return queryset 

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response( {"error":"Product cannot be deleted as it is associated with order item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return self.destroy(request, *args, *kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart__id=self.kwargs['cart_pk'])


class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    serializer_class = CartSerializer

    def get_serializer_context(self):
        return {'reques':self.request }
    
    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').filter(id=self.kwargs['pk'])


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all() 
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self ):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id =kwargs['pk']).count()>0:
            return Response( {"error":"collection cannot be deleted as it is associated with product item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {"product_id": self.kwargs['product_pk']}

    def get_queryset(self):
        return Review.objects.select_related('products').filter(product_id=self.kwargs['product_pk'])

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=["GET"], permission_classes=[ViewHistoryPermission])
    def history(self, request,pk):
        return Response("ok")

    @action(detail=False,methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get','patch', 'post', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH','POST','DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return  Order.objects.all()
        
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        # (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)  # Wrong way if used get_or_create
        return Order.objects.filter(customer_id=customer_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerialzer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerialzer(data=self.request.data, context = {'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data) 


    # def get_serializer_context(self):
    #     return {'request':self.request}

    # def get_serializer_class(self):
    #     return Order.objects.select_related('orderitem_set').filter()


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    
# class ProductList(ListCreateAPIView):

#     #1. attributes
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer


#     #2. overriding fns

#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()

#     # def get_serializer_class(self):
#     #     return ProductSerializer

#     def get_serializer_context(self):
#         return {'request':self.request}


#     # 3. Old approach with APIView inheritance

#     # def get(self, request):
#     #     queryset = Product.objects.select_related('collection').all() # To load the product and collections together
#     #     serializer = ProductSerializer(queryset, many=True,context={'request':request})
#     #     return Response(serializer.data)

#     # def post(self, request):
#     #     serializer = ProductSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     # print(serializer.validated_data)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset =  Product.objects.all()
#     serializer_class = ProductSerializer


#     def delete(self, request,pk, *args, **kwargs):
#         product = get_object_or_404(Product,pk=pk)
#         if product.orderitems.count() > 0:
#             return Response( {"error":"Product cannot be deleted as it is associated with order item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def get_serializer_context(self ):
#         return {'request':self.request}

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def get_serializer_context(self):
#         return {'request':self.request}

#     def delete(self, request,pk, *args, **kwargs):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')),pk=pk)
#         if collection.products.count() > 0:
#             return Response( {"error":"collection cannot be deleted as it is associated with product item"} ,status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
