from rest_framework import serializers
from apps.catalogs.infrastructure.models import LastOffer, Product, ProductVariant
from apps.catalogs.models import Category
from apps.inventory.serializers.front import StockRecordSerializer


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
        fields = ('id', 'title', 'categories', 'variants',
                  #   'product_image'
                  )


class ProductLastOfferSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name')
    product_category = serializers.CharField(source='product.categories',)
    product_original_price = serializers.CharField(source='product.price')
    # options = OptionProductSerializer(many = True , source = 'product.options')

    image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = LastOffer
        fields = ('id', 'product', 'product_name',
                  'product_category', 'offer_price',
                  'product_original_price', 'offer_time', 'image',
                  #   'options',
                  )

    def get_image_url(self, obj):
        request = self.context.get('request')
        photo_url = obj.product.images.first().image.url
        return request.build_absolute_uri(photo_url)


# class LastOfferSerializer(serializers.ModelSerializer):
#     # product_category = serializers.CharField(source='product.categories')
#     product_category = serializers.SlugRelatedField(
#         source='product.categories',
#         many=True,
#         read_only=True,
#         slug_field='title'
#     )
#     # options = OptionProductSerializer(many = True ,)
#     # company_name = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField('get_image_url')

#     def get_image_url(self, obj):
#         request = self.context.get('request')
#         photo_url = obj.product.images.first().image.image.url
#         return request.build_absolute_uri(photo_url)


#     # def get_company_name(self, obj):
#     #     cn = obj.company_name.company_name
#     #     return cn
#     class Meta:
#         model = ProductVariant
#         # fields = '__all__'
#         exclude=(
#             # "is_public",
#             # "balance",

#         )


class LastOfferSerializer(serializers.ModelSerializer):

    stock = StockRecordSerializer(
        source='stockrecord',
        read_only=True
    )

    product_name = serializers.CharField(
        source='product.title',
        read_only=True
    )

    product_category = serializers.SlugRelatedField(
        source='product.categories',
        many=True,
        read_only=True,
        slug_field='title'
    )

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')

        image = obj.product.images.first()

        if not image:
            return None

        url = image.image.image.url

        return request.build_absolute_uri(url) if request else url

    class Meta:
        model = ProductVariant
        fields = (
            'id',
            'product',
            'title',
            'sku',
            'product_name',
            'product_category',
            'stock',
            'image',
        )