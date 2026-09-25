from apps.catalogs.models import  ProductVariant
from django.contrib.auth import get_user_model

User = get_user_model()

class Cart():
    def __init__(self,request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session key if it exists:
        cart = self.session.get('session_key')
        
        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure cart is available on all pages of site
        self.cart = cart
    
    def db_add(self, variant, quantity):
        variant_id = str(variant.id)
        variant_qty = str(quantity)
        if variant_id in self.cart:
            pass
        else:
            # self.cart[variant_id] = {'price': str(variant.price)}
            self.cart[variant_id] = int(variant_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))
        
    
    def add(self,variant,quantity):
        variant_id = str(variant.id)
        variant_qty = str(quantity)
        if variant_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[variant_id] = int(variant_qty)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in = variant_ids)
        quantities = self.cart
        total = 0
        for key,value in quantities.items():
            key = int(key)
            for variant in variants:
                if variant.id == key:
                    if variant.stockrecord.in_offer:
                        total = total + (variant.stockrecord.offer_price * value)
                    else:
                        total = total + (variant.stockrecord.sale_price * value)
                    
        return total
            
        
    def __len__(self):
        return len(self.cart)
    
    def get_variants(self):
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(id__in = variant_ids)
        return variants
    
    
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self,variant, quantity):
        variant_id = str(variant.id)
        variant_qty= int(quantity)
        
        
        current_cart = self.cart
        
        current_cart[variant_id] = variant_qty
        
        self.session.modified = True
        
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))
        
        updated_cart = self.cart
        
        return updated_cart
    
    
    def delete(self,variant):
        variant_id = str(variant.id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            
        self.session.modified =  True
        
        if self.request.user.is_authenticated:
            # Get the current user profile:
            current_user = User.objects.filter(id = self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # Save carty to the Customer Model:
            current_user.update(old_cart=str(carty))