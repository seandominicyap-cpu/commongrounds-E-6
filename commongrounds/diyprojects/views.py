from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q
from .models import Project, ProjectCategory, Favorite, ProjectReview, ProjectRating, Profile    
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import ReviewForm

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
            
            created_ids = list(created.values_list('id', flat=True))
            favorited_ids = list(favorited.values_list('id', flat=True))
            reviewed_ids = list(reviewed.values_list('id', flat=True))
            excluded_ids = set(created_ids + favorited_ids + reviewed_ids)
            
            context['all_projects'] = Project.objects.exclude(id__in=excluded_ids)
            
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'diyprojects/projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile
        context['avg_rating'] = self.object.ratings.aggregate(Avg('score'))['score__avg']
        context['favorite_count'] = Favorite.objects.filter(project=self.object).count()
        context['review_form'] = ReviewForm()
        context['is_favorited'] = Favorite.objects.filter(project=self.object, profile=user_profile).exists()


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
    
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = 'diyprojects/projects/project_form.html'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user.profile.role != "Project Creator" or project.creator != request.user.profile:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()
    
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'diyprojects/registration/signup.html'

def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    favorite, created = Favorite.objects.get_or_create(
        project=project, 
        profile=request.user.profile
    )
    
    if not created:
        favorite.delete()
    return redirect('diyprojects:project_detail', pk=pk)

def add_review(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST) 
        
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.reviewer = request.user.profile
            review.save()
            return redirect('diyprojects:project_detail', pk=pk)
        else:
            print(f"Form Errors: {form.errors}") 
            print(f"Post Data received: {request.POST}")
            
    return redirect('diyprojects:project_detail', pk=pk)

def rate_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        score = request.POST.get('score')

        if score:
            ProjectRating.objects.update_or_create(
                project=project,
                profile=request.user.profile,
                defaults={'score': int(score)}
            )
    return redirect('diyprojects:project_detail', pk=pk)


