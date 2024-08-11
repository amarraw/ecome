from django.urls import path
from ecomeapp import views
from .views import Index , Cart , CheckOut , Orders
from ecomeapp.middlewares.auth import auth_middleware

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("contact/", views.contact, name="contact"),
    path("seller/", views.seller, name="seller"),
    path('cart/', Cart.as_view(), name="cart"),
    path('checkout/',CheckOut.as_view(), name="checkout"),
    path('orders/', auth_middleware(Orders.as_view()) , name="orders"),

]
