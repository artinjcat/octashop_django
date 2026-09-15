from rest_framework import serializers
from apps.catalogs.infrastructure.models import LastOffer, Product
from apps.catalogs.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ['id', 'name', 'slug', 'parent', 'image', 'description']
        fields = '__all__'
        
        

# class OptionProductSerializer(serializers.ModelSerializer):
    
    
#     class Meta:
#         model = OptionProduct
#         fields = "__all__"
        

class ProductSerializer(serializers.ModelSerializer):
    
    # product_image = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='images'
    # )
    class Meta:
        model = Product
        fields = ('id','title','category',
                #   'product_image'
                  )
        
        
        
        
class ProductLastOfferSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name')
    product_category = serializers.CharField(source='product.category.category')
    product_original_price = serializers.CharField(source='product.price')
    # options = OptionProductSerializer(many = True , source = 'product.options')
    
    image = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = LastOffer
        fields = ('id','product','product_name',
                  'product_category','offer_price',
                  'product_original_price','offer_time','image',
                #   'options',
                  )
        
    def get_image_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.product.images.first().image.url
        return request.build_absolute_uri(photo_url)
        
        
class LastOfferSerializer(serializers.ModelSerializer):
    product_category = serializers.CharField(source='category.category')
    # options = OptionProductSerializer(many = True ,)
    company_name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField('get_image_url')
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.images.first().image.url
        return request.build_absolute_uri(photo_url)
    
    
    def get_company_name(self, obj):
        cn = obj.company_name.company_name
        return cn
    class Meta:
        model = Product
        # fields = '__all__'
        exclude=(
            "is_public",
            "balance",
            
        )