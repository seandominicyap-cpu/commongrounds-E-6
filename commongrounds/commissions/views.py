"""Views for commissions project."""

from .models import Commission, JobApplication, Job, ApplicationStatus
from django.views.generic import TemplateView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from .forms import JobFormSet, CommissionForm
from .services import update_commission_status
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
        commission = get_object_or_404(Commission, pk=commission_id)
        maker = commission.maker or None
        status = commission.status.__str__
        jobs = Job.objects.filter( 
            commission = commission 
        ).annotate( 
            accepted_count=Count(
                "job_applications",
                filter=Q(job_applications__status__name="ACCEPTED")
            )
        )
        total_manpower = (
            Job.objects.filter(commission=commission)
            .aggregate(total=Sum("manpower_required"))
        )["total"] or 0
        
        accepted_status = ApplicationStatus.objects.get(name="ACCEPTED")

        signed_manpower = JobApplication.objects.filter(
            job__commission = commission,
            status=accepted_status
        ).count()

        open_manpower = total_manpower - signed_manpower

        ctx["title"] = commission.title
        ctx["description"] = commission.description
        ctx["type"] = commission.commission_type.name
        ctx["people_required"] = commission.people_required
        ctx["jobs"] = jobs
        ctx["status"] = commission.status
        ctx["total_manpower"] = total_manpower
        ctx["open_manpower"] = open_manpower
        ctx["maker"] = maker
        ctx["pk"] = commission_id
        ctx["status"] = status
        return ctx


class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """View to create commissions."""
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_create.html"
    success_url = "/commissions/requests/list"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.POST:
            ctx["job_formset"] = JobFormSet(self.request.POST)
        else:
            ctx["job_formset"] = JobFormSet()

        return ctx

    def form_valid(self, form):
        form.instance.maker = self.request.user.profile
        response = super().form_valid(form)

        job_formset = JobFormSet(self.request.POST, instance=self.object)

        if job_formset.is_valid():
            job_formset.save()
        else:
            print(job_formset.errors)

        return response

    
class CommissionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    """View to update commissions."""
    model = Commission
    form_class = CommissionForm
    template_name = "commissions/commission_update.html"
    success_url = "/commissions/requests/list"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.request.POST:
            ctx["job_formset"] = JobFormSet(self.request.POST, instance=self.object)
        else:
            ctx["job_formset"] = JobFormSet(instance=self.object)

        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context["job_formset"]

        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()

            update_commission_status(self.object)
            
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

