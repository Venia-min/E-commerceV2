from rest_framework import serializers
from ecommerce.inventory.models import (
    Product,
    ProductInventory,
    Brand,
    ProductAttributeValue,
    Media,
    Category,
)


class MediaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ["image", "alt_text"]
        read_only = True

    def get_image(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        exclude = ["id"]
        depth = 2


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["name"]


class AllProducts(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only = True
        editable = False


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ["name"]
        read_only = True
        editable = False


class ProductInventorySerializer(serializers.ModelSerializer):
    # brand = BrandSerializer(many=False, read_only=True)
    # attribute = ProductAttributeValueSerializer(source="attribute_values", many=True)
    # image = MediaSerializer(source="media_product_inventory", many=True)

    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "sku",
            # "image",
            "store_price",
            "is_active",
            "product",
            # "product_type",
            # "brand",
            # "attribute",
        ]
        read_only = True
        depth = 2
