"""Views for commissions project."""

from .models import Commission, JobApplication, Job
from django.views.generic import TemplateView
# Create your views here.


class CommissionListView(TemplateView):
    """View to list commissions."""

    template_name = "commissions/commissions_list.html"

    def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            user_profile = user.profile
            created = Commission.objects.filter(maker=user_profile)
            applied = Commission.objects.filter(
                        jobs__job_applications__applicant=user_profile
                    ).distinct()
            other = Commission.objects.exclude(
                id__in=created.values("id")
            ).exclude(
                id__in=applied.values("id")
            )
        else:
            created = Commission.objects.none()
            applied = Commission.objects.none()
            other = Commission.objects.all()
        
        ctx["created_commissions"] = created
        ctx["applied_commissions"] = applied
        ctx["other_commissions"] = other
        return ctx


class CommissionDetailView(TemplateView):
    """View to show commissions details."""

    template_name = "commissions/commissions_detail.html"

    def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        commission_id = int(self.kwargs.get("pk"))
        commission = Commission.objects.filter(pk=commission_id).first()
        ctx["title"] = commission.title
        ctx["type"] = commission.commission_type.name
        ctx["people_required"] = commission.people_required
        ctx["description"] = commission.description
        return ctx


class CommissionCreateView(TemplateView):
    """View to create commissions."""
    template_name = "commissions/commissions_create.html"


class CommissionUpdateView(TemplateView):
    """View to update commissions."""
    template_name = "commissions/commissions_update.html"
