from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Service, Cart, CartItem, Order, OrderItem
from .forms import UserRegistrationForm
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, OrderForm

def home(request):
    return render(request, 'main/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'main/profile.html', {'orders': orders})

def catalog(request):
    products = Product.objects.all()
    services = Service.objects.all()
    return render(request, 'main/catalog.html', {'products': products, 'services': services})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'main/cart.html', {'items': items})

@login_required
def add_to_cart(request, product_id=None, service_id=None):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = None
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    elif service_id:
        service = get_object_or_404(Service, id=service_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service)
    else:
        return redirect('catalog')
    
    # Если товар или сервис уже есть в корзине, не увеличиваем количество
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.cart.user == request.user:
        cart_item.delete()
    return redirect('cart')

@login_required
def order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, service=item.service, quantity=item.quantity)
            items.delete()
            # Получаем список заказанных товаров для передачи в order_success
            cart_items = order.orderitem_set.all()
            return render(request, 'main/order_success.html', {'cart_items': cart_items})
    else:
        form = OrderForm()
    
    return render(request, 'main/form_order.html', {'form': form})




def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'main/product_detail.html', {'product': product})

def form_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order_success')
    else:
        form = OrderForm()
    
    return render(request, 'main/form_order.html', {'form': form})


def order_success(request):
    # Получаем список заказанных товаров из параметров запроса
    cart_items = request.GET.getlist('cart_items')
    return render(request, 'main/order_success.html', {'cart_items': cart_items})
    
