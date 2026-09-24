from math import e

from django.core.cache import cache
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login , logout
from django.contrib.auth.models import User
import sms_ir
from apps.cart.cart import Cart
from auth.users.forms import SignUpForm,ChangePasswordForm
from decouple import config
from django.contrib import messages
from apps.catalogs.models import Category
import json
import secrets

from sms_ir import SmsIr

# from carts.cart import Cart


User = get_user_model()


def sub_category_list():
    return Category.objects.filter(depth=1, is_public=True).order_by("title")

def login_user(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        if User.objects.filter(phone_number = phone_number).exists():
            requested_user = get_object_or_404(User,phone_number = phone_number)
            password = request.POST["password"]
            user = authenticate(request, username=requested_user.username, password=password)
            if user is not None:
                login(request, user)
                
                
                current_user = User.objects.get(id=request.user.id)
                saved_cart = current_user.old_cart
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    cart = Cart(request)
                    
                    for key,value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)
                return redirect("home-site:home")
            else:
                messages.success(request, "دوباره تلاش کنید 1")
                return redirect("users-site:login")
        else:
            messages.success(request, "دوباره تلاش کنید 2")
            return render(request,"accounts/login.html",{})
    else:
        messages.success(request, "دوباره تلاش کنید 3")
        return render(request,"accounts/login.html",{})

def logout_user(request):
    logout(request)
    return redirect("home-site:home")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            
            
            try:
                
                phone_number = form.cleaned_data["phone_number"]
                
                # username = form.cleaned_data["username"]
                # password = form.cleaned_data["password1"]
                # user = User.objects.get(username = username)
                # customer = User.objects.create(user = user, phone_number = request.POST.get("phone_number"))
                # user_auth = authenticate(username = username, password = password)
                # login(request, user_auth)
                
                
                
                request.session["verify_phone"] = phone_number
                
                otp = secrets.randbelow(90000) + 10000
                cache.set(phone_number, otp, timeout=120)  # Cache the OTP for 2 minutes
                sms_ir = SmsIr(
                    config('SMS_IR_API_KEY'),config('LINE_NUMBER')
                )
                # sms_ir.send_sms(phone_number, f"کد تایید شما در نیلی طب: {otp}")
                print(f"OTP for {phone_number}: {otp}")  # For debugging purposes
            
            except Exception as e:
                print(f"Error sending SMS: {e}")
                messages.error(request, "خطا در ارسال پیامک. لطفاً دوباره تلاش کنید.")
                return render(request, "accounts/register.html", {})
            
            form.save()
            
            
            
            
            return redirect("users-site:verify-phone-number" )
        else:
            messages.error(request, form.errors)
            return render(request, "accounts/register.html", {})
    else:
        return render(request, "accounts/register.html", {})
    
    
    
    
    
def verify_phone_number(request):
    phone_number = request.session.get("verify_phone")
    if request.method == "POST":
        entered_otp = request.POST.get("digits")
        cached_otp = cache.get(phone_number)
        print(f"Entered OTP: {entered_otp}, Cached OTP: {cached_otp}")  # Debugging line
        if cached_otp and str(cached_otp) == entered_otp:
            
            # OTP is valid, proceed with user registration
            user = get_object_or_404(User, phone_number=phone_number)
            if user.is_active == False:
                user.is_active = True
                user.save()
            
            # Log the user in after successful verification
            login(request, user)
            
            # Clear the session variable
            del request.session["verify_phone"]
            
            return redirect("home-site:home")
        else:
            messages.error(request, "کد وارد شده اشتباه است یا منقضی شده است.")
            return render(request, "accounts/verify-phone-number.html", {"phone_number": phone_number})
    
    
    return render(request, "accounts/verify-phone-number.html", {"phone_number": phone_number})





def profile_user(request):
    if request.user.is_authenticated:
        context = {}
        context["sub_categories"] = sub_category_list()
        return render(request, "accounts/profile.html", context)
    else:
        return redirect("users-site:login")
    
def edit_profile_user(request):
    if request.user.is_authenticated:
        context = {}
        context["sub_categories"] = sub_category_list()
        return render(request, "accounts/edit-profile.html", context)
    
    
    
def update_password(request):
    context = {}
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
                login(request, current_user)
                return redirect("users-site:profile")
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                return redirect("users-site:update-password")
        else:
            context["form"] = ChangePasswordForm(current_user)
            return render(request, "accounts/update-password.html", context)
    else:
        return redirect("users-site:login")
    
    
    
def favorites(request):
    if request.user.is_authenticated:
        context={}
        context["sub_categories"] = sub_category_list()
        return render(request, "accounts/favorites.html", context)
        
    else:
        return redirect("users-site:login")
    
    
def rules_page(request):
    context={}
    context["sub_categories"] = sub_category_list()
    return render(request, "accounts/rules.html", context)


