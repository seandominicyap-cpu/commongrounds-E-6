from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
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