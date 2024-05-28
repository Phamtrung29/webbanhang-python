
from django.shortcuts import render,redirect,  get_object_or_404
from django.http import HttpResponse, JsonResponse # HttpResponse Lớp này được sử dụng để tạo ra một phản hồi HTTP từ một view function trong Django(hiển thị từ view sang html). 
from . models import * #import tất cả các model từ module hiện tại của ứng dụng Django
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import LoginForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import CartItem, Product,  Order, OrderItem

# Create your views here.
def get_home(request):
    products = Product.objects.all()
    users = User.objects.all()
    return render(request, 'app/home.html', {'products': products, 'users': users})

def cart(request):
    context= {}
    return render(request, 'app/cart.html', context)
def about(request):
    context= {}
    return render(request, 'app/about.html', context)

def shop(request):
    products = Product.objects.all()  # Truy vấn tất cả sản phẩm từ cơ sở dữ liệu
    return render(request, 'app/shop.html', {'products': products})

def contact(request):
    context= {}
    return render(request, 'app/contact.html', context)

def productdetail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'app/productdetail.html', {'product': product})
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'app/login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {'form': form})

def logoutpage(request):
    logout(request)
    return redirect("login")

from django.shortcuts import render
from .models import Product, CartItem, Order, OrderItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Tìm hoặc tạo mới một mục trong giỏ hàng
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product_name=product.name, price=product.price, image_url=product.image_url)
    
    # Nếu mục đã tồn tại, tăng số lượng lên 1
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.subtotal = cart_item.price  # Khởi tạo subtotal khi tạo mới mục
    
    # Tính toán lại subtotal và lưu mục vào cơ sở dữ liệu
    cart_item.subtotal = cart_item.price * cart_item.quantity
    cart_item.save()

    return redirect('cart')

def cart(request):
    shipping_cost = 10
    cart_items = CartItem.objects.filter(user=request.user)
    cart_subtotal = sum(item.subtotal for item in cart_items)
    total_price = sum(item.subtotal for item in cart_items) + shipping_cost
    return render(request, 'app/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart_subtotal': cart_subtotal})




def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        quantity = int(request.POST.get('quantity'))

        # Kiểm tra xem sản phẩm có tồn tại trong giỏ hàng không
        cart_item = get_object_or_404(CartItem, pk=product_id)

        # Kiểm tra xem user hiện tại có quyền cập nhật số lượng sản phẩm không (nếu cần)
        if cart_item.user != request.user:
            return redirect('cart')

        # Cập nhật số lượng sản phẩm trong giỏ hàng
        cart_item.quantity = quantity
        cart_item.subtotal = cart_item.price * quantity
        cart_item.save()

        return redirect('cart')

    return redirect('cart')


def remove_from_cart(request, item_id):
    # Lấy CartItem từ database dựa trên item_id
    cart_item = get_object_or_404(CartItem, pk=item_id)

    # Kiểm tra xem user hiện tại có quyền xóa sản phẩm không (nếu cần)
    if cart_item.user != request.user:
        return redirect('cart')

    # Xóa sản phẩm khỏi giỏ hàng
    cart_item.delete()

    return redirect('cart')




def checkout(request):
    if request.method == 'POST':
        # Lấy thông tin giỏ hàng của người dùng
        cart_items = CartItem.objects.filter(user=request.user)

        # Kiểm tra giỏ hàng trống
        if not cart_items.exists():
            return redirect('cart')

        shipping_cost = 10  # Giả sử phí vận chuyển là 10
        cart_subtotal = sum(item.subtotal for item in cart_items)

        # Tạo một đơn hàng mới
        order = Order.objects.create(user=request.user, total_amount=cart_subtotal + shipping_cost)

        # Chuyển các mục từ giỏ hàng sang đơn hàng
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product_name=cart_item.product_name,
                price=cart_item.price,
                quantity=cart_item.quantity,
                subtotal=cart_item.subtotal
            )

        # Xóa các mục trong giỏ hàng
        cart_items.delete()

        # Thực hiện xử lý thanh toán (nếu cần)

        return render(request, 'app/checkout.html', {'order': order})

    return redirect('cart')


def order_detail(request):
    if request.method == 'POST':
        # Lấy thông tin từ biểu mẫu
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment')

        # Lấy đơn hàng mới nhất
        order = Order.objects.last()

        # Lưu thông tin chi tiết đơn hàng
        order_detail = OrderDetail.objects.create(
            order=order,
            name=name,
            email=email,
            address=address,
            phone=phone,
            payment_method=payment_method,
            paid= True
        )


        # Chuyển hướng người dùng đến trang xác nhận đặt hàng hoặc trang chính của ứng dụng
        return redirect('success_order')  # Thay 'home' bằng tên định danh của trang xác nhận đặt hàng nếu cần

    return render(request, 'app/checkout.html')

def success_order(request):
    return render(request, 'app/success_order.html')

def myorder(request):
    # Lấy tất cả các đơn hàng của người dùng hiện tại
    orders = Order.objects.filter(user=request.user)
    orders_with_detail = OrderDetail.objects.filter(order__user=request.user)

    return render(request, 'app/myorder.html', {'orders': orders, 'orders_with_detail': orders_with_detail})

from django.contrib import messages

def delete_order(request, order_id):
    try:
        # Xóa thông tin chi tiết đơn hàng trong OrderDetail (nếu có)
        OrderDetail.objects.filter(order_id=order_id).delete()

        # Xóa các mục trong OrderItem
        OrderItem.objects.filter(order_id=order_id).delete()
        
        # Xóa đơn hàng
        Order.objects.filter(id=order_id).delete()
        
        messages.success(request, "Order and related details have been deleted successfully.")
        return redirect('myorder')  # Chuyển hướng đến trang myorder sau khi xóa thành công
    except Exception as e:
        messages.error(request, f"An error occurred while deleting order: {str(e)}")
        return redirect('myorder')  # Chuyển hướng đến trang myorder nếu có lỗi xảy ra
    

def search(request):
    query = request.GET.get('q')  # Lấy dữ liệu tìm kiếm từ request
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |  # Tìm kiếm theo tên sản phẩm
            Q(brand__icontains=query) |  # Tìm kiếm theo thương hiệu
            Q(description__icontains=query)  # Tìm kiếm theo mô tả
        )
    else:
        results = Product.objects.all()  # Nếu không có tìm kiếm, hiển thị tất cả sản phẩm
    return render(request, 'app/search.html', {'results': results, 'query': query})