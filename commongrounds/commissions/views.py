"""Views for commissions project."""
from .models import Commission
from django.views.generic import TemplateView
# Create your views here.


class CommissionListView(TemplateView):
    """View to list commissions."""

    template_name = "commissions/commissions_list.html"

    def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        ctx["commissions"] = Commission.objects.all()
        return ctx


class CommissionDetailView(TemplateView):
    """View to show commissions details."""

    template_name = "commissions/commissions_detail.html"

    def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        commission_id = int(self.kwargs.get('pk'))
        commission = Commission.objects.filter(pk=commission_id).first()
        ctx["title"] = commission.title
        ctx["type"] = commission.commission_type.name
        ctx["people_required"] = commission.people_required
        ctx["description"] = commission.description
        return ctx
