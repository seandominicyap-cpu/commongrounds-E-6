from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "merchstore/item_list.html"
    context_object_name = "items"


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/item_detail.html"
    context_object_name = "item"
