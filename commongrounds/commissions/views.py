"""Views for commissions project"""
from django.shortcuts import render
from .models imnport Commission, CommissionType
from django.views.generic import TemplateView
# Create your views here.


class CommissionListView(TemplateView):
    """View to list commissions"""
    template_name = "commissions/commissions_list.html"

    def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        ctx["commissions"] = Commission.objects.all()
        return ctx


class CommissionDetailView(TemplateView):
    """View to show commissions details"""
    template_name = "commissions/commissions_detail.html"

        def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        commission_id = int(self.kwargs.get('pk'))
        commission = Recipe.objects.filter(pk=recipe_id).first()
        ctx["title"] = commission
        ctx["type"] = commission
        ctx["people_required"] = commission
        ctx["description"] = commission
        return ctx