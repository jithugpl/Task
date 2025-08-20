# store/serializers.py
from rest_framework import serializers
from .models import Product, Category, CartItem, Cart, Order,User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # Nested representation
    class Meta:
        model = Cart
        fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True)
#     class Meta:
#         model = Order
#         fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            cart_item = CartItem.objects.create(**item_data)
            order.items.add(cart_item)
        return order