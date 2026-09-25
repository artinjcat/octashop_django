from django.shortcuts import render, get_object_or_404
from apps.cart.cart import Cart

from django.http import JsonResponse
from django.shortcuts import redirect

from apps.cart.forms import CheckOutOrderForm
from apps.catalogs.models import Category, Product , ProductVariant
from apps.payments.models import OrderedVariant



def sub_category_list():
    return Category.objects.filter(depth=1, is_public=True).order_by("title")

class CartView():
    def cart_summary(request):
        context = {}
        context["sub_categories"] = sub_category_list()
        cart = Cart(request)
        
        if cart.__len__() == 0:
            return render(request, "carts/cart_empty.html",context)
        else:
            cart_variants = cart.get_variants()
            context["cart_variants"] = cart_variants
            quantities = cart.get_quants()
            context["quantities"] = quantities
            totals = cart.cart_total()
            context["totals"] = totals
            return render(request, "carts/cart_summary.html",context)
        
        
    def cart_add(request):
        cart = Cart(request)
        if request.POST.get("action")== "post":
            variant_id = request.POST.get("product_id")
            product_qty = request.POST.get("qty-to-cart")
            variant = get_object_or_404(ProductVariant,id=variant_id)
            cart.add(variant=variant, quantity=product_qty)
            cart_quantity = cart.__len__()
            
            
            # response = JsonResponse({ 'product name :': '{}  {}'.format(product.company_name, product.model)} )
            response = JsonResponse({ 'qty': cart_quantity} )
            
            return response
        
        
        
        
        
    def cart_delete(request):
        cart = Cart(request)
        if request.POST.get("action")== "remove-cart":
            variant_id = request.POST.get("variant_id")
            variant = get_object_or_404(ProductVariant, id=variant_id)
            cart.delete(variant=variant)
            response = JsonResponse({'variant':variant_id})
            return response
        else:
            pass
    
    
    def cart_update(request):
        cart = Cart(request)
        if request.POST.get("action")== "update-cart":
            variant_id = request.POST.get("variant_id")
            variant_qty = request.POST.get("qty_update")
            variant = get_object_or_404(ProductVariant, id=variant_id)
            
            cart.update(variant=variant, quantity=variant_qty)
            response = JsonResponse({'qty':variant_qty})
            return response
        
        
class CartCheckOutView():
    def checkout_template_view(request):
        if request.user.is_authenticated:
            context = {}
            context["sub_categories"] = sub_category_list()
            cart = Cart(request)
            if cart.__len__() == 0:
                return render(request, "carts/cart_empty.html",context)
            else:
                cart_variants = cart.get_variants
                context["cart_variants"] = cart_variants
                quantities = cart.get_quants()
                context["quantities"] = quantities
                totals = cart.cart_total()
                context["totals"] = totals
            if request.method == "POST":
                form = CheckOutOrderForm(request.POST)
                if form.is_valid:
                    try:
                        order = form.save(commit=False)
                        order.user = request.user
                        order.save()
                        cart_v = cart.get_variants()
                        cart_q = quantities
                        
                        for variant in cart_v:
                            quantity = cart_q[str(variant.id)]
                            op = OrderedVariant.objects.create(
                            order = order,
                            variant = variant,
                            quantity = quantity,
                            )
                            
                            op.save()
                            cart.delete(variant)
                        # return redirect("orders-view")
                        return redirect("payments-site:order-view", pk = order.id)
                    except Exception as error:
                        print(error)
                        print("Error occurred while processing the order.")
                        
                        return redirect("users-site:profile")
                else:
                    return redirect("checkout")
            else:
                return render(request, 'carts/checkout.html', context)
        else:
            return redirect("users-site:login")
        
