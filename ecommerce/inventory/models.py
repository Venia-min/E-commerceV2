from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Inventory Category table implemented with MPTT
    """

    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("category name"),
        help_text=_("format: required, max-100"),
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("category safe URL"),
        help_text=_("format: required, letters, numbers, underscore, or hyphens"),
    )
    is_active = models.BooleanField(
        default=False,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        unique=False,
        blank=True,
        verbose_name=_("parent of category"),
        help_text=_("format: not required"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product details table
    """

    web_id = models.CharField(
        max_length=50,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("product website ID"),
        help_text=_("format: required, unique"),
    )
    slug = models.SlugField(
        max_length=255,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("product safe URL"),
        help_text=_("format: required, letters, numbers, underscores, or hyphens"),
    )
    name = models.CharField(
        max_length=255,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("product name"),
        help_text=_("format: required, max-255"),
    )
    description = models.TextField(
        null=False,
        unique=False,
        blank=True,
        verbose_name=_("product description"),
        help_text=_("format: required"),
    )
    category = models.ForeignKey(
        Category,
        related_name="product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        null=False,
        unique=False,
        blank=False,
        default=False,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date product created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date product last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Brand table
    """

    name = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("brand name"),
        help_text=_("format: required, unique, max-255"),
    )

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
    Product attribute table
    """

    name = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("product attribute name"),
        help_text=_("format: required, unique, max-255"),
    )
    description = models.TextField(
        null=False,
        unique=False,
        blank=True,
        verbose_name=_("product attribute description"),
        help_text=_("format: required"),
    )

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Product type table
    """

    name = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("type of product"),
        help_text=_("format: required, unique, max-255"),
    )
    product_type_attributes = models.ManyToManyField(
        ProductAttribute,
        related_name="product_type",
        through="ProductTypeAttribute",
    )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
    Product attribute value table
    """

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute_value",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        max_length=255,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("attribute value"),
        help_text=_("format: text or numbers, required, max-255"),
    )

    def __str__(self):
        return f"{self.product_attribute.name} : {self.attribute_value}"


class ProductInventory(models.Model):
    """
    Product inventory table
    """

    sku = models.CharField(
        max_length=20,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("stock keeping unit"),
        help_text=_("format: required, unique, max-20"),
    )
    upc = models.CharField(
        max_length=12,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_("universal product code"),
        help_text=_("format: required, unique, max-12"),
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="product_inventory",
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Product,
        related_name="product_inventory",
        on_delete=models.PROTECT,
    )
    brand = models.ForeignKey(
        Brand,
        related_name="product_inventory",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="productinventory",
        through="ProductAttributeValues",
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible, default=false"),
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("default product"),
        help_text=_("format: true=default product, default=false"),
    )
    retail_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("recommended retail price"),
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    store_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("regular store price"),
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    is_digital = models.BooleanField(
        default=False,
        verbose_name=_("product is digital"),
        help_text=_("format: true=product is digital, default=false"),
    )
    weight = models.FloatField(
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("product weight"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date sub-product created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date sub-product updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return self.sku


class Media(models.Model):
    """
    Product image table
    """

    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="media",
    )
    img_url = models.ImageField(
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("product image"),
        upload_to="images/",
        help_text=_("format: required, default-default.png"),
    )
    alt_text = models.CharField(
        max_length=255,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("alternative text"),
        help_text=_("format: required, max-255"),
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=_("product default image"),
        help_text=_("format: default=false, true=default image"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date image added"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date image updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class Stock(models.Model):
    """
    Product stock table
    """

    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="stock",
        on_delete=models.PROTECT,
    )
    last_checked = models.DateTimeField(
        null=True,
        unique=False,
        blank=True,
        verbose_name=_("inventory stock check date"),
        help_text=_("format: Y-m-d H:M:S, null-true, blank-true"),
    )
    units = models.IntegerField(
        default=0,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("units/qty of stock"),
        help_text=_("format: required, default-0"),
    )
    units_sold = models.IntegerField(
        default=0,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("units sold to data"),
        help_text=_("format: required, default-0"),
    )


class ProductAttributeValues(models.Model):
    """
    Product attribute values link table
    """

    attributevalues = models.ForeignKey(
        ProductAttributeValue,
        related_name="product_attribute_values",
        on_delete=models.PROTECT,
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="attributevalues",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)


class ProductTypeAttribute(models.Model):
    """
    Product type link table
    """

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="producttype",
        on_delete=models.PROTECT,
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name="attribute",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("product_attribute", "product_type"),)
