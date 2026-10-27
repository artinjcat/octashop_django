from django.db import models    
from auth.profiles.infrastructure.models import Profile


class ProfileAssetType(models.Model):
    type = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=64)


    def __str__(self):
        return "{} ({})".format(self.name, self.type)
    

class ProfileAsset(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assets')
    type = models.ForeignKey(ProfileAssetType, on_delete=models.CASCADE, related_name='assets')
    amount = models.DecimalField(default = 0 ,max_digits=20, decimal_places=8)
    
    
    
    class Meta:
        unique_together = ('user_profile', 'type')
        


    def __str__(self):
        return self.user_profile.username + " - " + self.type.type + " - " + str(self.amount)


class AssetHistoryType(models.Model):
    name = models.CharField(max_length=32 , unique=True)

    def __str__(self):
        return self.name


class ProfileAssetHistory(models.Model):
    profile_asset = models.ForeignKey(ProfileAsset, on_delete=models.CASCADE, related_name='history')
    change_type = models.ForeignKey(AssetHistoryType, on_delete=models.CASCADE, related_name='history')
    change_amount = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
    class Meta:
        verbose_name = 'Profile Asset History'
        verbose_name_plural = 'Profile Asset Histories'

    def __str__(self):
        return f"{self.profile_asset.user_profile.username} - {self.change_type.name} - {self.change_amount} - {self.timestamp}"