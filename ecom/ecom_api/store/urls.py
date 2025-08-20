from django.urls import path
from . import views


   
urlpatterns = [
    path('auth/register/', views.register, name='register'),
      path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/create/', views.product_create, name='product-create'),
    path('cart/<int:user_id>/', views.cart_detail, name='cart-detail'),
    path('cart/<int:user_id>/add/', views.add_to_cart, name='add-to-cart'),
    path('orders/<int:user_id>/', views.order_list, name='order-list'),
    path('orders/<int:user_id>/create/', views.create_order, name='create-order'),
]
