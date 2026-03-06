from django.db import models


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    descrpition = models.TextField

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='category', null=True, blank=True)
    description = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    steps = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_materials_list(self):
        return self.materials.splitlines()

    def get_steps_list(self):
        return self.steps.splitlines()

    class Meta:
        ordering = ['created_on']
