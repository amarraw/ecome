from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import gererate_token, TokenGenrator
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from time import sleep
from django.contrib.auth.forms import PasswordChangeForm
from order.models import Order
from django.contrib.auth import authenticate, login, logout, get_user_model

def call_me(request):
    if request.method == "POST":
        messages.success(request,f"we will get you soon {request.user.first_name + " " + request.user.last_name}")
        return redirect("profile")

class Profile(View):
    def post(self, request):
        if request.user.is_authenticated:
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request, "Password changed successfully!")
                return redirect("/auth/login/")  # Redirect after successful password change
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, "authuser/profile.html", {"form": fm})

    def get(self, request):
        if request.user.is_authenticated:
            fm = PasswordChangeForm(user=request.user)
            customer = request.session.get('User')
            orders = Order.get_orders_by_customer(customer)
            return render(request, 'authuser/profile.html', {'form': fm, 'orders': orders})
        else:
            return redirect("/auth/login/") 

def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["pass1"]
        confirm_password = request.POST["pass2"]

        if password == confirm_password:
            try:
                if User.objects.get(username=email):
                    messages.info(request, "Email already taken")
                    return render(request, "authuser/login.html")
            except Exception as e:
                pass
            user = User.objects.create_user(email, email, password)
            user.is_active = False
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            email_subject = "Active your Account"
            message = render_to_string(
                "activate.html",
                {
                    "user": user,
                    "domain": "http://127.0.0.1:8000",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": gererate_token.make_token(user),
                },
            )
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, [email]
            )
            email_message.send()
            messages.success(request, "please active your account via email ")

            return redirect("/auth/login/")
        else:
            messages.warning(request, "Password Doesn,t match")
            return redirect("/auth/signup/")
    return render(request, "authuser/signup.html")


class ActivateAccountViews(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user is not None and gererate_token.check_token(user, token):
            user.is_active = True
            user.save()
            sleep(1)
            messages.info(request, "Account Activated Successfully !!")
            return redirect("/auth/login/")
        return render(request, "404.html")


User = get_user_model()


class user_login(View):

    return_url = None

    def get(self, request):
        user_login.return_url = request.GET.get("return_url")
        return render(request, "authuser/login.html")

    def post(self, request):
        username = request.POST.get("email", None)
        userpass = request.POST.get("pass1", None)

        try:
            user = User.objects.get(email=username)
            if user.is_active == False:
                messages.info(request, "User account is inactive")
                return redirect("/auth/login/")
        except User.DoesNotExist:
            messages.info(request, "Invalid Credentials")
            return redirect("/auth/login/")

        myuser = authenticate(username=username, password=userpass)

        if myuser is not None:
            login(request, myuser)
            request.session["User"] = user.id
            messages.success(request, "Login Successfully!")
            if user_login.return_url:
                return HttpResponseRedirect(user_login.return_url)
            else:
                user_login.return_url = None
                return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("/auth/login/")


def handlelogout(request):
    logout(request)
    messages.info(request, "logout successfully!!")
    return redirect("/")


def page_not_found(request):
    return render(request, "404.html")


def changepass(request):
    if request.user.is_authenticated:
        fm = PasswordChangeForm(user=request.user)
        if request.method == "POST":
            fm = PasswordChangeForm(user=request.user, data=request.POST)

            if fm.is_valid():
                fm.save()
                messages.success(request, "password change successfully!!")
                redirect("/auth/login/")
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, "changepass.html", {"form": fm})

    return redirect("/auth/login/")
