
from django.contrib import admin
from django.urls import path
from home import views as home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.get_home, name="home"),
    path('cart/', home.cart, name="cart"),
    path('about/', home.about, name="about"),
    path('shop/', home.shop, name="shop"),
    path('contact/', home.contact, name="contact"),
    path('product/<int:product_id>/', home.productdetail, name="productdetail"),
    path('register/', home.signup,name="register"),
    path('login/', home.user_login, name="login"),
    path('logout/', home.logoutpage, name="logout"),
    path('search/', home.search, name='search'),
    path('add-to-cart/<int:product_id>/', home.add_to_cart, name='add_to_cart'),
    path('update-cart/', home.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', home.remove_from_cart, name='remove_from_cart'),
    path('checkout/', home.checkout, name="checkout"),
    path('order/', home.order_detail, name="order_detail"),
    path('success_order/', home.success_order, name="success_order"),
    path('myorder/', home.myorder, name="myorder"),
    path('delete_order/<int:order_id>/', home.delete_order, name='delete_order'),
]
