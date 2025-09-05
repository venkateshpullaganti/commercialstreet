from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, 'products',lookup='product')
products_router.register('reviews',views.ReviewViewSet, basename='product-reviews')

router.register('carts', views.CartViewSet, basename='cart')
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', views.CartItemViewSet, basename='cart-items')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('orders', views.OrderViewSet, basename='orders')


urlpatterns = router.urls + products_router.urls + cart_router.urls

# urlpatterns = [
#     path("products/",views.ProductList.as_view()),
#     path('products/<int:pk>/',views.ProductDetails.as_view()),
#     path('collections/',views.CollectionList.as_view()),
#     path('collections/<int:pk>/',views.CollectionDetail.as_view(), name='collection-detail'),
# ]