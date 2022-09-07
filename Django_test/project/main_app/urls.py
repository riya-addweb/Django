from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from .views import *


app_name = "main_app"

router = DefaultRouter()
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"product", views.ProductViewSet, basename="product")
router.register(r"product/<product_id>/category/<category_id>", views.AddProductViewSet, basename="add-product")


urlpatterns = [
    path("", include(router.urls)),
    path("product/<int:product_id>/category/<int:category_id>/", AddProductViewSet.as_view({'post': 'update'}), name="add-product"),
]
