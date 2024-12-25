from elasticsearch_dsl.serializer import serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, mixins

from ecommerce.inventory.models import Category, Product, ProductInventory
from ecommerce.drf.serializer import (
    AllProducts,
    ProductInventorySerializer,
    CategorySerializer,
    ProductSerializer,
)


class CategoryList(APIView):
    """
    Return list of all categories
    """

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class ProductByCategory(APIView):
    """
    Return product by category
    """

    def get(self, request, query=None):
        queryset = Product.objects.filter(category__slug=query)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductInventoryByWebId(APIView):
    """
    Return Sub Product by WebId
    """

    def get(self, requst, query=None):
        queryset = ProductInventory.objects.filter(product__web_id=query)
        serializer = ProductInventorySerializer(queryset, many=True)
        return Response(serializer.data)
