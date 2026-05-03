from django.shortcuts import redirect
from django.urls import reverse
from merchstore.models import Transaction


class BaseTransactionStrategy:
    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the execute method.")


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        existing_transaction = Transaction.objects.filter(
            buyer=request.user.profile, product=product, status="On cart"
        ).first()

        if existing_transaction:
            added_amount = form.cleaned_data["amount"]
            existing_transaction.amount += added_amount
            existing_transaction.save()
            product.stock = max(0, product.stock - added_amount)
            if product.stock == 0:
                product.status = "Out of stock"
            elif product.status == "Out of stock" and product.stock > 0:
                product.status = "Available"
            product.save()
        else:
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
