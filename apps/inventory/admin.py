from django.contrib import admin

from apps.inventory.models import StockRecord,StockMovement

@admin.register(StockRecord)
class StockRecordAdmin(admin.ModelAdmin):
    list_display = ('variant', 'buy_price', 'sale_price', 'in_offer', 'offer_price', 'stock', 'reserved')
    search_fields = ('variant__title',)
    list_filter = ('in_offer',)
    
    
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('stock_record', 'quantity', 'movement_type', 'created_at')
    search_fields = ('stock_record__variant__title',)
    list_filter = ('movement_type', 'created_at')