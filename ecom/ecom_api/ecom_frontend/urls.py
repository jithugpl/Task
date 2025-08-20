from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("products/", views.product_list, name="product_list"),
    path('products/add/', views.add_product, name='add_product'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('orders/', views.order_list, name='order_list'),

]
