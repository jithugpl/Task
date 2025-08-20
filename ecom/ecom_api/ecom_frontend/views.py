from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
#         cart_item = serializer.save(cart=cart)
@login_required
def order_list(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'ecom_frontend/order_list.html', {'orders': orders})

@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # For simplicity, always buy 1 quantity
    quantity = 1
    total_price = product.price * quantity

    Order.objects.create(
        buyer=request.user,
        product=product,
        quantity=quantity,
        total_price=total_price
    )

    return redirect('order_list')
# --- Existing views ---
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user   # logged-in user as owner
            product.save()
            return redirect('product_list')  # redirect after save
    else:
        form = ProductForm()
    return render(request, 'ecom_frontend/add_product.html', {'form': form})
def home(request):
    return render(request, 'home.html')

def index(request):
    print("Index view called")
    return render(request,'index.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {"error": "Invalid credentials"})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')
def product_list(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})


# --- New serializer ---
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


# --- New API view ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



