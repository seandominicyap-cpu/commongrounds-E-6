from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RoleRequiredMixin

# Create your views here.
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'profile_form.html'

    def get_success_url(self):
        return f"/accounts/{self.object.user.username}/"

    def get_object(self):
        return Profile.objects.get(user__username=self.kwargs['username'])