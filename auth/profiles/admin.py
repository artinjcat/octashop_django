from django.contrib import admin

from auth.profiles.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id','user__username',
        )
    # inlines = [InlineProfileAsset]
    # readonly_fields = ('id', 'user__username', )
    # search_fields = ('user__username', 'user__email')
    # list_filter = ('location',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    

    