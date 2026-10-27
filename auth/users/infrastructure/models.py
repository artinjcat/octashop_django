
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels





class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    
    
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    old_cart = models.CharField(_("Shopping cart"), max_length=200, null=True, blank=True)
    date_joined = jmodels.jDateTimeField(auto_now_add=True, blank=True, null=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.username
    
    
    # def get_jalali_date(self):
    #         return date2jalali(self.user.date_joined)
    
    
    
    
