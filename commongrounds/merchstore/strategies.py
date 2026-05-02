from django.shortcuts import redirect
from django.urls import reverse


class BaseTransactionStrategy:
    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the execute method.")


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        transaction = form.save(commit=False)
        transaction.product = product
        transaction.buyer = request.user.profile
        transaction.status = "On cart"
        transaction.save()
        return redirect("merchstore:cart")


class GuestPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        request.session["pending_transaction"] = {
            "product_id": product.pk,
            "amount": form.cleaned_data["amount"],
        }
        login_url = reverse("login")
        next_url = product.get_absolute_url()
        return redirect(f"{login_url}?next={next_url}")
