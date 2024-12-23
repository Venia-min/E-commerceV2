from django.contrib import admin
from django.urls import path, include

from ecommerce.drf.views import CategoryList, ProductByCategory

# from rest_framework import routers
# from ecommerce.drf import views
# from ecommerce.search.views import SearchProductInventory


# router = routers.DefaultRouter()
# router.register(r"api", views.AllProductViewSet, basename="allproducts")
# router.register(
#     r"product/(?P<slug>[^/.]+)", views.ProductInventoryViewSet, basename="products"
# )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/inventory/category/all", CategoryList.as_view()),
    path("api/inventory/products/category/<str:query>/", ProductByCategory.as_view()),
    # path("demo/", include("ecommerce.demo.urls", namespace="demo")),
    # path("", include(router.urls)),
    # path("search/<str:query>/", SearchProductInventory.as_view()),
]
