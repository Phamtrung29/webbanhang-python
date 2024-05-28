from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render,redirect
# Create your models here.
from django import forms
#change forms register django

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=200)  # Thêm trường mới để lưu đường dẫn đến ảnh
    star = models.IntegerField(default=0)

    def image_path(self):
        return f'static/img/products/{self.image_url}'  # Hàm này trả về đường dẫn đầy đủ đến ảnh

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=200, default='')
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s cart item - {self.product_name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


class OrderDetail(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(max_length=100)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
