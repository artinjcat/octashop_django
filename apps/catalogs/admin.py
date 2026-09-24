from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from apps.catalogs.infrastructure.models import ProductAbout, ProductBrand, ProductImage, ProductVariant

from .models import (Option,
                     ProductClass,
                     Category, ProductAttribute, ProductRecommendation, Product, ProductAttributeValue)


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(Option)


class AttributeCountFilter(admin.SimpleListFilter):
    title = 'attribute count'
    parameter_name = 'attribute_count'

    def lookups(self, request, model_admin):
        return (
            ('0', 'No attributes'),
            ('1', 'Has attributes'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(products_attributes__isnull=True)
        elif self.value() == '1':
            return queryset.filter(products_attributes__isnull=False)
        return queryset


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1




@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'track_stock',
                    'require_shipping', 'has_attributes')
    list_filter = ('track_stock', 'require_shipping', AttributeCountFilter)
    prepopulated_fields = {'slug': ('title',)}
    # Add the inline for product attributes and recommendations
    inlines = [ProductAttributeInline]
    actions = []



class ProductRecommendationInline(admin.TabularInline):
    model = ProductRecommendation
    extra = 1
    fk_name = 'primary'  # Specify the foreign key field to use for the inline


class ProductCategoryInline(admin.StackedInline):
    model = Product.categories.through
    extra = 2
    
class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 2
    
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    
class ProductAboutInline(admin.TabularInline):
    model = ProductAbout
    extra = 1
    max_num = 5  # Limit to one instance per product
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    inlines = [
        ProductAttributeValueInline,
        ProductImageInline,
        ProductAboutInline,
        ProductRecommendationInline,
        ]
    prepopulated_fields = {"slug": ("title",)}
    
    
    
@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {"slug": ("title",)}
    
    
    
    
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'product_class',)
    list_filter = ('product_class',)
    search_fields = ('title', 'type',)
    
    
@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ('primary', 'recommendation',)
    list_filter = ('primary__product_class',)
    search_fields = ('primary__title', 'recommendation__title',)
    
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'sku',)
    list_filter = ('product',)
    search_fields = ('title', 'sku',)
    
    
@admin.register(ProductAbout)
class ProductAboutAdmin(admin.ModelAdmin):
    list_display = ('product', 'title',)
    list_filter = ('product',)
    search_fields = ('title', 'description',)