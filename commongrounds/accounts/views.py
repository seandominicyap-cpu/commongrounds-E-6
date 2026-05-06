from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from bookclub.models import Book
from commissions.models import Commission
from diyprojects.models import Project
from localevents.models import Event
from merchstore.models import Product
# Create your views here.
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["display_name"]
    template_name = "profile_form.html"

    def get_success_url(self):
        return f"/accounts/{self.object.user.username}/"

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs["username"])


class RegisterView(TemplateView):
    template_name = "register.html"
    def get(self, request):
        return render(request, "register.html", {
            "user_form": UserCreationForm(),
        })

    def post(self, request):
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            user_form.save()

            return redirect("login")

        return render(request, "register.html", {
            "user_form": user_form,
        })
    

class DashboardView(TemplateView):
    template_name = "dashboard.html"
    def get_context_data(self, **kwargs):
        """Get context data."""
        ctx = super().get_context_data(**kwargs)
        user = self.request.user.profile

        created_books = Book.objects.filter(contributor=user)
        created_commissions = Commission.objects.filter(maker=user)
        created_projects = Project.objects.filter(creator=user)
        created_events = Event.objects.filter(organizers=user)
        created_products = Product.objects.filter(owner=user)
        ctx["created_books"] = created_books
        ctx["created_commissions"] = created_commissions
        ctx["created_projects"] = created_projects
        ctx["created_events"] = created_events
        ctx["created_products"] = created_products
        return ctx
        