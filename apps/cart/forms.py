from django import forms
from apps.payments.models import Order,OrderedVariant



class CheckOutOrderForm(forms.ModelForm):
    
    
    class Meta:
        model = Order
        fields = ("national_code","first_name","last_name","address","postal_code", "phone_number", "description")
        
class OrderProductForm(forms.ModelForm):
    
    class Meta:
        model = OrderedVariant
        fields = ()
