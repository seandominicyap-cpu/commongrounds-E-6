from django import forms
from .models import ProjectReview, Project, ProjectRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'What did you think of this project?',
                'class': 'form-control'
            }),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'category'] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your project...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }