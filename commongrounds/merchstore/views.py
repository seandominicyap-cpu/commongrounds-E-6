from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views import View
from accounts.decorators import role_required
from accounts.mixins import RoleRequiredMixin
from merchstore.models import Product, ProductType, Transaction
from merchstore.strategies import AuthenticatedPurchaseStrategy, GuestPurchaseStrategy


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]


class ProductForm(forms.ModelForm):
    new_product_type = forms.CharField(
        max_length=255,
        required=False,
        label="Create new product type",
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "product_type",
            "new_product_type",
            "product_image",
            "description",
            "price",
            "stock",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product_type"].required = False


class ProductListView(ListView):
    model = Product
    template_name = "merchstore/item_list.html"
    context_object_name = "all_products"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and "pending_transaction" in request.session:
            pending = request.session.pop("pending_transaction")
            try:
                product = Product.objects.get(pk=pending["product_id"])
                if product.owner != request.user.profile:
                    existing_transaction = Transaction.objects.filter(
                        buyer=request.user.profile, product=product, status="On cart"
                    ).first()

                    if existing_transaction:
                        existing_transaction.amount += pending["amount"]
                        existing_transaction.save()
                    else:
                        Transaction.objects.create(
                            buyer=request.user.profile,
                            product=product,
                            amount=pending["amount"],
                            status="On cart",
                        )
            except Product.DoesNotExist:
                pass

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        is_seller = False
        if user.is_authenticated and hasattr(user, "profile"):
            user_profile = user.profile
            is_seller = user_profile.roles.filter(name="Market Seller").exists()
            context["user_products"] = Product.objects.filter(owner=user_profile)
            context["all_products"] = Product.objects.exclude(owner=user_profile)
        else:
            context["user_products"] = None
            context["all_products"] = Product.objects.all()

        context["is_seller"] = is_seller
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/item_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = kwargs.get("form", TransactionForm())
        user = self.request.user

        is_seller = False
        if user.is_authenticated and hasattr(user, "profile"):
            is_seller = user.profile.roles.filter(name="Market Seller").exists()

        if self.object.stock > 0:
            form.fields["amount"].widget.attrs.update(
                {
                    "min": 1,
                    "max": self.object.stock,
                    "value": 1,
                }
            )

        context["form"] = form
        context["is_seller"] = is_seller
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TransactionForm(request.POST)

        if self.object.stock > 0:
            form.fields["amount"].widget.attrs.update(
                {"min": 1, "max": self.object.stock}
            )

        if form.is_valid():
            requested_amount = form.cleaned_data["amount"]
            if requested_amount > self.object.stock:
                form.add_error(
                    "amount", f"Only {self.object.stock} items left in stock."
                )
                return self.render_to_response(self.get_context_data(form=form))

            if request.user.is_authenticated:
                strategy = AuthenticatedPurchaseStrategy()
            else:
                strategy = GuestPurchaseStrategy()

            return strategy.execute(request, self.object, form)

        return self.render_to_response(self.get_context_data(form=form))


class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/product_form.html"
    allowed_roles = ["Market Seller"]

    def get_success_url(self):
        return reverse_lazy("merchstore:item_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        new_type_name = form.cleaned_data.get("new_product_type")

        if new_type_name:
            product_type, created = ProductType.objects.get_or_create(
                name=new_type_name.strip()
            )
            form.instance.product_type = product_type
        elif not form.cleaned_data.get("product_type"):
            form.add_error(
                "product_type",
                "Please select an existing product type or enter a new one.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)


class ProductUpdateView(RoleRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "merchstore/product_form.html"
    allowed_roles = ["Market Seller"]

    def get_success_url(self):
        return reverse_lazy("merchstore:item_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        product = form.save(commit=False)
        new_type_name = form.cleaned_data.get("new_product_type")

        if new_type_name:
            product_type, created = ProductType.objects.get_or_create(
                name=new_type_name.strip()
            )
            product.product_type = product_type
        elif not form.cleaned_data.get("product_type"):
            form.add_error(
                "product_type",
                "Please select an existing product type or enter a new one.",
            )
            return self.form_invalid(form)

        if product.stock == 0:
            product.status = "Out of stock"
        elif product.status == "Out of stock" and product.stock > 0:
            product.status = "Available"

        product.save()
        return super().form_valid(form)


class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()
        categorized = {}
        for transaction in transactions:
            seller = transaction.product.owner
            if seller not in categorized:
                categorized[seller] = []
            categorized[seller].append(transaction)

        context["categorized_transactions"] = categorized
        return context


class CartItemDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        transaction = get_object_or_404(
            Transaction, pk=pk, buyer=request.user.profile, status="On cart"
        )

        product = transaction.product
        product.stock += transaction.amount
        if product.status == "Out of stock" and product.stock > 0:
            product.status = "Available"

        product.save()
        transaction.delete()

        return redirect("merchstore:cart")


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(product__owner=self.request.user.profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()
        categorized = {}
        for transaction in transactions:
            buyer = transaction.buyer
            if buyer not in categorized:
                categorized[buyer] = []
            categorized[buyer].append(transaction)

        context["categorized_transactions"] = categorized
        return context


@login_required
@role_required(["Market Seller"])
def product_create_fbv(request):
    if request.method == "POST":
        pass

    return render(request, "merchstore/product_form.html")


@login_required
@role_required(["Market Seller"])
def product_update_fbv(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        pass

    return render(request, "merchstore/product_form.html", {"object": product})
