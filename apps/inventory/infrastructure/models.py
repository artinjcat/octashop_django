from django.db import models
from django.db import transaction




    
class StockMovement(models.Model):

    class MovementType(models.TextChoices):
        PURCHASE = "purchase", "Purchase"
        SALE = "sale", "Sale"
        RETURN = "return", "Return"
        DAMAGE = "damage", "Damage"
        ADJUSTMENT = "adjustment", "Adjustment"
        INITIAL = "initial", "Initial Stock"

    stock_record = models.ForeignKey(
        'inventory.StockRecord',
        on_delete=models.PROTECT,
        related_name="movements",
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
    )

    quantity = models.IntegerField()

    quantity_before = models.PositiveIntegerField()

    quantity_after = models.PositiveIntegerField()

    note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return (
            f"{self.stock_record.variant} | "
            f"{self.movement_type} | "
            f"{self.quantity}"
        )
        
        
        
        
class StockRecord(models.Model):
    variant = models.OneToOneField('catalogs.ProductVariant', on_delete=models.CASCADE, related_name='stockrecord',null=True, blank=True)
    buy_price = models.PositiveBigIntegerField(null=True, blank=True)
    sale_price = models.PositiveBigIntegerField()
    in_offer = models.BooleanField(default=False)
    offer_price =  models.PositiveBigIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(
        default=0,
    )
    threshold_low_stock = models.PositiveIntegerField(null=True, blank=True)
    # partner = models.ForeignKey('partners.Partner', on_delete=models.CASCADE, related_name='stockrecords')
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    
    
    class Meta:
      verbose_name = 'Stock Record'
      verbose_name_plural = 'Stock Records'
      
      

    def __str__(self):
        return f"{self.variant} - {self.variant.sku}"
  
  
    @transaction.atomic
    def increase_stock(
        self,
        quantity,
        movement_type=StockMovement.MovementType.PURCHASE,
        note="",
    ):
        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        stock_record = (
            StockRecord.objects
            .select_for_update()
            .get(pk=self.pk)
        )

        stock_before = stock_record.stock

        stock_record.stock += quantity

        stock_record.save(
            update_fields=[
                "stock",
                "updated_at",
            ]
        )

        StockMovement.objects.create(
            stock_record=stock_record,
            movement_type=movement_type,
            quantity=quantity,
            quantity_before=stock_before,
            quantity_after=stock_record.stock,
            note=note,
        )
        self.stock = stock_record.stock
        return self.stock
    
    
    
    
    @transaction.atomic
    def decrease_stock(
        self,
        quantity,
        movement_type=StockMovement.MovementType.SALE,
        note="",
    ):
        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        stock_record = (
            StockRecord.objects
            .select_for_update()
            .get(pk=self.pk)
        )

        if quantity > stock_record.stock:
            raise ValueError(
                "Insufficient stock."
            )

        stock_before = stock_record.stock

        stock_record.stock -= quantity

        stock_record.save(
            update_fields=[
                "stock",
                "updated_at",
            ]
        )

        StockMovement.objects.create(
            stock_record=stock_record,
            movement_type=movement_type,
            quantity=-quantity,
            quantity_before=stock_before,
            quantity_after=stock_record.stock,
            note=note,
        )

        self.stock = stock_record.stock
        return self.stock
    
    
    @property
    def available_stock(self):
        return max(0, self.stock - self.reserved)