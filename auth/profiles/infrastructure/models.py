from django.db import models
from django.contrib.auth import get_user_model
from django_jalali.db import models as jmodels

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' , blank=True, null=True,)
    birthday = jmodels.jDateField(  null=True, blank=True ,
                                  verbose_name="تاریخ تولد",
                                  help_text="تاریخ تولد را به صورت شمسی وارد کنید. (مثال: 1370/01/01)")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    
    # referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_profiles')
    # is_active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # old_cart = models.CharField(_("Shopping cart"), max_length=200, null=True, blank=True)


    def __str__(self):
        return self.user.username if self.user else "Profile without user"
    
    
    # def save(self, *args, **kwargs):
    #     if self.pk is not None:
    #         old_value = TelegramProfile.objects.get(pk=self.pk).referred_by
    #         if old_value != self.referred_by:
    #             raise ValidationError("You cannot change the referred_by field after creation.")
    #     super().save(*args, **kwargs)
    