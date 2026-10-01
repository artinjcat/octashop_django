from rest_framework import serializers
from apps.inventory.models import StockRecord

# class StockRecordSerializer(serializers.ModelSerializer):
     
#     class Meta:
#         model = StockRecord
#         fields = (
#             'id',
#             'product_variant',
            
#             'sale_price',
#             'in_offer',
#             'offer_price',
#             'offer_time',
#             'stock',
#             'is_active',
#         )
     
class StockRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockRecord
        fields = (
            'id',
            'variant',
            'sale_price',
            'in_offer',
            'offer_price',
            'stock',
            'reserved',
            'available_stock',
        )