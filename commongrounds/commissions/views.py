"""Views for commissions project."""

from .models import Commission, JobApplication, Job, ApplicationStatus
from django.views.generic import TemplateView, CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum, Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import RoleRequiredMixin
from .forms import JobFormSet, CommissionForm
from django.http import HttpResponseForbidden

from .services import update_commission_status, CommissionService
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
        summary = CommissionService.get_commission_summary(commission)

        ctx["title"] = commission.title
        ctx["description"] = commission.description
        ctx["type"] = commission.commission_type.name
        ctx["people_required"] = commission.people_required
        ctx["jobs"] = jobs
        ctx["status"] = commission.status
        ctx["total_manpower"] = summary["total_manpower"]
        ctx["open_manpower"] = summary["open_manpower"]
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
            ctx["job_formset"] = JobFormSet(self.request.POST, prefix="jobs")
        else:
            ctx["job_formset"] = JobFormSet(prefix="jobs")

        return ctx

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context["job_formset"]

        if job_formset.is_valid():
            jobs_data = []

            for job_form in job_formset:
                if job_form.cleaned_data and not job_form.cleaned_data.get("DELETE", False):
                    jobs_data.append({
                        "role": job_form.cleaned_data["role"],
                        "manpower_required": job_form.cleaned_data["manpower_required"],
                        "status": job_form.cleaned_data["status"],
                    })
            form.cleaned_data.pop("maker", None)
            self.object = CommissionService.create_commission(
                author=self.request.user.profile,
                data=form.cleaned_data,
                jobs_data=jobs_data
            )

            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))

    
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

            CommissionService.sync_commission_status(self.object)

            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))


class ApplyToJobView(LoginRequiredMixin, View):

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)

        try:
            CommissionService.apply_to_job(
                applicant=request.user.profile,
                job=job
            )
        except ValueError:
            return HttpResponseForbidden("Cannot apply")

        return redirect("commissions:commission_detail", pk=job.commission.pk)