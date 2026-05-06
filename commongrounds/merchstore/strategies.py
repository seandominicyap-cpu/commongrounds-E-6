from django.shortcuts import redirect
from django.urls import reverse
from merchstore.models import Transaction


class BaseTransactionStrategy:
    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the execute method.")


class AuthenticatedPurchaseStrategy(BaseTransactionStrategy):
    def execute(self, request, product, form):
        user_profile = request.user.profile
        amount = form.cleaned_data["amount"]

        transaction, created = Transaction.objects.get_or_create(
            buyer=user_profile,
            product=product,
            status="On cart",
            defaults={"amount": amount},
        )

        if not created:
            transaction.amount += amount
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
