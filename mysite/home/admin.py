from django.contrib import admin
from .models import Product, Order, OrderDetail, OrderItem, CartItem, LoginForm, SignUpForm

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(OrderItem)
admin.site.register(CartItem)