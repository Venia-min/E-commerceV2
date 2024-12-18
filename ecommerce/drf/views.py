from ecommerce.inventory.models import Product
from rest_framework import viewsets, permissions, mixins
from ecommerce.drf.serializer import AllProduct


class AllProductViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):

    queryset = Product.objects.all()
    serializer_class = AllProduct
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
