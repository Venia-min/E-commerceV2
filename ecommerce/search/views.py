from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from elasticsearch_dsl import Q

from ecommerce.drf.serializer import ProductInventorySearchSerializer
from ecommerce.search.documents import ProductInventoryDocument


class SearchProductInventory(APIView, LimitOffsetPagination):
    """
    View for search in product.name, product.web_id, brand.name
    endpoint: api/search/<str:query>/
    """

    productinventory_serializer = ProductInventorySearchSerializer
    search_document = ProductInventoryDocument

    def get(self, request, query):
        try:
            q = Q(
                "multi_match",
                query=query,
                fields=["product.name", "product.web_id", "brand.name"],
                fuzziness="auto",
            ) & Q(
                should=[
                    Q("match", is_default=True),
                ],
                minimum_should_match=1,
            )

            search = self.search_document.search().query(q)
            response = search.execute()

            result = self.paginate_queryset(response, request, view=self)
            serializer = self.productinventory_serializer(result, many=True)
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
