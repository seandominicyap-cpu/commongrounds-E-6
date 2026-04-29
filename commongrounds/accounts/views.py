from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Profile

# Create your views here.
class PostUpdateView(UpdateView):
    model = Profile
    fields = ['display_name']
    template_name = 'profile_form.html'