from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' , blank=True, null=True,)
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
    