from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Cart, CartItem, Order
# from .serializers import ProductSerializer
# Create your views here.
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer
from .serializers import CartItemSerializer

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, password=password)
    return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request, user_id):
    if request.user.id != user_id:  # Prevent other users from seeing your cart
        return Response({'error': 'Not allowed'}, status=403)
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

# @api_view(['GET'])
# def cart_detail(request, user_id):
#     try:
#         cart = Cart.objects.get(user_id=user_id)
#     except Cart.DoesNotExist:
#         return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = CartSerializer(cart)
#     return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request, user_id):
    try:
        cart = Cart.objects.get(user_id=user_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user_id=user_id)

    serializer = CartItemSerializer(data=request.data)
    if serializer.is_valid():
        cart_item = serializer.save()
        cart.items.add(cart_item)
        cart.save()
        return Response({'success': 'Item added to cart'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Retrieve a single product by ID
@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# Create a new product
@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from .models import Order

# @api_view(['POST'])
# def create_order(request, user_id):
#     serializer = OrderSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user_id=user_id)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_order(request, user_id):
#     data = request.data.copy()
#     data['user'] = user_id  # Add user automatically
#     serializer = OrderSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'success': 'Order created'}, status=201)
#     return Response(serializer.errors, status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request, user_id):
    if request.user.id != user_id:
        return Response({'error': 'Not allowed'}, status=403)

    data = request.data.copy()
    data['user'] = request.user.id
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': 'Order created'}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def order_list(request, user_id):
    orders = Order.objects.filter(user_id=user_id)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)