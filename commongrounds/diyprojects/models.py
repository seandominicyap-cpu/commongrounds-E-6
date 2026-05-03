from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [('Project Creator', 'Project Creator'), ('Regular User', 'Regular User')]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Regular User')

    def __str__(self):
        return self.user.username

class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    descrpition = models.TextField

    def __str__(self):
        return self.name
    
    class Meta: 
        ordering = ['name']
        

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, related_name='category', null=True, blank=True)
    
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

    description = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    steps = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)   
    updated_on = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.title
    
    def get_materials_list(self):
        return self.materials.splitlines()

    def get_steps_list(self):
        return self.steps.splitlines()

    class Meta: 
        ordering = ['-created_on']

class Favorite(models.Model):
    STATUS_CHOICES = [('Backlog', 'Backlog'), ('To-do', 'To-do'), ('Done', 'Done')]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_favorited = models.DateField(auto_now_add=True)
    project_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Backlog')

    def __str__(self):
        return f"{self.profile} favorited {self.project}"
    
class ProjectReview(models.Model):
    project = models.ForeignKey(Project, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='project_reviews/', blank=True, null=True)

    def __str__(self):
        return f"Review by {self.reviewer} on {self.project}"

class ProjectRating(models.Model):
    project = models.ForeignKey(Project, related_name='ratings', on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    def __str__(self):
        return f"{self.score}/10 by {self.profile}"

