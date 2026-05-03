from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    CartView,
    TransactionListView,
    CartItemDeleteView,
)

app_name = "merchstore"

urlpatterns = [
    path("items", ProductListView.as_view(), name="item_list"),
    path("item/<int:pk>", ProductDetailView.as_view(), name="item_detail"),
    path("item/add", ProductCreateView.as_view(), name="item_add"),
    path("item/<int:pk>/edit", ProductUpdateView.as_view(), name="item_edit"),
    path("cart", CartView.as_view(), name="cart"),
    path("cart/remove/<int:pk>", CartItemDeleteView.as_view(), name="cart_remove"),
    path("transactions", TransactionListView.as_view(), name="transaction_list"),
]
