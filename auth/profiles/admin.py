from django.contrib import admin

from auth.profiles.models import Profile

from django_jalali.admin.filters import JDateFieldListFilter

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        # 'id',
        'user__username',
        'birthday',
        # ('birthday', JDateFieldListFilter),
        )
    # inlines = [InlineProfileAsset]
    # readonly_fields = ('id', 'user__username', )
    # search_fields = ('user__username', 'user__email')
    list_filter = (
        ('birthday', JDateFieldListFilter),
        )
    # widgets = {
    #     'birthday': jadmin.widgets.AdminSplitjDateTime,
    # }

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    

    