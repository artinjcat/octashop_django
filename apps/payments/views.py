from datetime import datetime
from django.shortcuts import render,redirect
from django.http import JsonResponse

from apps.catalogs.infrastructure.models import Category
import jdatetime
from .models import *




def sub_category_list():
    return Category.objects.filter(depth=1, is_public=True).order_by("title")


class Payment():
    def orders_page(request):
        if request.user.is_authenticated:
            context={}
            context["sub_categories"] = sub_category_list()
            if Order.objects.filter(user = request.user).exists:
                context["orders"] = Order.objects.filter(user = request.user).order_by("-id")
                return render(request, "accounts/profile-order.html", context)
            else:
                return render(request, "carts/cart_empty.html",context)
        else:
            return redirect("users-site:login")
    
    
    
    
    
    def order_view(request,pk):
        context = {}
        context["sub_categories"] = sub_category_list()
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(id=pk)
                if order.user == request.user:
                    context["order"] = order
                    total_price = 0
                    for ordered_variant in order.ordered_variants.all():
                        if ordered_variant.variant.stockrecord.in_offer:
                            total_price = (ordered_variant.variant.stockrecord.offer_price * ordered_variant.quantity) + total_price
                        else:
                            total_price = (ordered_variant.variant.stockrecord.sale_price * ordered_variant.quantity) + total_price

                    context["total_price"] = total_price
                    return render(request, "payments/order-page.html", context)
                else:
                    return redirect("login")
            except Exception as error:
                print(error)
                print("Order Not Found")
                return redirect("home-site:home")
        else:
            return redirect("users-site:login")
        
    def upload_receipt_url(request):
        if request.user.is_authenticated:
            if request.method == "POST" and request.POST.get("action") == "post":
                
                order_id = request.POST.get("order")
                if Order.objects.filter(id=order_id, user=request.user).exists:
                    order=Order.objects.get(id=order_id)
                    order.receipt = request.FILES.get("img")
                    order.payment_status = True
                    order.order_date_done = jdatetime.datetime.now()
                    total_price = 0
                    for variant in order.ordered_variants.all():
                        if variant.variant.stockrecord.in_offer:
                            total_price = (variant.variant.stockrecord.offer_price * variant.quantity) + total_price
                        else:
                            total_price = (variant.variant.stockrecord.sale_price * variant.quantity) + total_price
                    order.total_price = total_price
                    
                    order.save()
                else:
                    context = {"status":"failed","details":"Order Not Found"}
                    response = JsonResponse(context)
                    return response
                context = {"status":"success"}
                response = JsonResponse(context)
                return response
            else:
                print("get")
        else:
            pass
        
        



# def payment(request):
#     if request.user.is_authenticated:
#         context={}
#         context["sub_categories"] = sub_category_list()
        
#         return render(request, "accounts/payment.html", context)
#     else:
#         return redirect("login")