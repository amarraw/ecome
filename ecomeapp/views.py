from django.shortcuts import render , redirect
from .models import Contact , Product
from .forms import ContactForm
from django.contrib import messages
from math import ceil
from django.views import View 
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from order.models import Order


# Create your views here.

class Index(View):
    def get(self, request):
        return render(request,'index.html')
    def post(self, request):
        product_id = request.POST.get('product_id')
        remove = request.POST.get('remove')
        cart = request.session.get('cart',{})
        product_id = str(product_id)

        if product_id in cart:
            if remove:
                cart[product_id] -=1
                if cart[product_id] <= 0:
                    del cart[product_id]
            else:
                cart[product_id] += 1
        else:
            cart[product_id]=1


        request.session['cart'] = cart

        # print(request.session['cart'] )
        
        return redirect('index')
    

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        allProds =[]
        catprods = Product.objects.values('category','id')
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prod= Product.objects.filter(category=cat)
            n=len(prod)
            nSlids = n // 4 + ceil(n/4) - (n//4)
            allProds.append([prod, range(1, nSlids),nSlids])

        l1 = list(request.session.get('cart').keys())
        total = len(l1)
        # print(total)
        parms = {"allProds":allProds,
                 "total" : total,      
                 }

        return render(request, "index.html",parms)      

def contact(request):
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "We will get back to you soon ...")
            return redirect('contact')  # Use the name of your URL pattern for the contact page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, "contact.html", {'form': form})

def seller(request):
    return render(request, "seller.html")

class Cart(View):
    def get(self , request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'cart.html' ,{"products":products} )

class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        # print(User)
        customer = request.session.get('User')
        print(customer)
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(products)

        print(address, phone , )
        if customer is not None:
                for product in products:
                    print(product.id)
                    order = Order(customer = User(id = customer), 
                            product = product,
                            price = product.price,
                            address = address,
                            phone = phone,
                            quantity = cart.get(str(product.id)))
                    order.save()
                request.session['cart'] = {}
                messages.success(request,'Your order successfully placed')
        else:
            messages.success(request,'login is required')
            return redirect('user_login')
        
        return redirect('cart')
    def get(self, request):
        return render(request,'order.html')




class Orders(View):
    def get(self, request):

        customer = request.session.get('User')
        orders = Order.get_orders_by_customer(customer)
        
        return render(request, 'order.html',{'orders':orders})
    
