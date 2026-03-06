from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = ''
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = ''
    

