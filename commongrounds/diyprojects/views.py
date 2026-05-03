from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import Project, ProjectCategory, Favorite, ProjectReview, ProjectRating, Profile    

class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/projects/project_list.html'
    context_object_name = 'all_projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_authenticated:
            profile = user.profile
            
            created = Project.objects.filter(creator=profile)
            favorited = Project.objects.filter(favorite__profile=profile)
            reviewed = Project.objects.filter(reviews__reviewer=profile).distinct()
            
            context['created_projects'] = created
            context['favorited_projects'] = favorited
            context['reviewed_projects'] = reviewed
            
            excluded_ids = (created | favorited | reviewed).values_list('id', flat=True)
            context['all_projects'] = Project.objects.exclude(id__in=excluded_ids)
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'diyprojects/projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avg_rating'] = self.object.ratings.aggregate(Avg('score'))['score__avg']
        context['favorite_count'] = Favorite.objects.filter(project=self.object).count()
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = 'diyprojects/projects/project_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.role == "Project Creator":
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
    
class ProjectUpdateView():
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = 'diyprojects/project/project_form.html'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user.profile.role != "Project Creator" or project.creator != request.user.profile:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()