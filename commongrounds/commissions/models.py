"""Models of commmissions app."""

from django.db import models
from accounts.models import Profile
# Create your models here.
class JobStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        verbose_name = "Job Status"
        verbose_name_plural = "Job Statuses"

    def __str__(self):
        return self.name


class ApplicationStatus(models.Model):
    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        verbose_name = "Application Status"
        verbose_name_plural = "Application Statuses"

    def __str__(self):
        return self.name

    
def get_default_job_status():
    return JobStatus.objects.get(name='OPEN').id

def get_default_application_status():
    return JobStatus.objects.get(name='PENDING').id
    

class CommissionType(models.Model):
    """Model that represents commission type."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    

    class Meta:
        """Class that provides ordering of commission types."""

        ordering = ["name"]
        verbose_name = "Commission Type"
        verbose_name_plural = "Commission Types"


class Commission(models.Model):
    """Model that represents commissions."""

    title = models.CharField(max_length=255)
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions",
    )
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        JobStatus,
        on_delete=models.PROTECT,
        null=True,
        default=get_default_job_status
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
    def refresh_status(self):
        full = JobStatus.objects.get(name="FULL")

        if self.jobs.exists() and all(j.status == full for j in self.jobs.all()):
            self.status = full
        else:
            self.status = JobStatus.objects.get(name="OPEN")

        self.save(update_fields=["status"])


    class Meta:
        """Class that provides ordering of commissions."""

        ordering = ["created_on"]
        verbose_name = "Commission"
        verbose_name_plural = "Commissions"

        
class Job(models.Model):
    commission = models.ForeignKey(
        Commission,
        on_delete = models.CASCADE,
        related_name = 'jobs'
    )

    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.ForeignKey(
        JobStatus,
        on_delete=models.PROTECT,
        null=True,
        default=get_default_job_status
    )

    def __str__(self):
        return self.role
    

    class Meta:
        ordering = ["-status", "-manpower_required", "role"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"


class JobApplication(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete = models.CASCADE,
        related_name = 'job_applications'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete = models.CASCADE,
        related_name = 'job_applications'
    )
    status = models.ForeignKey(
        ApplicationStatus,
        on_delete = models.PROTECT,
        related_name = "job_applications",
        null=True,
        default=get_default_application_status
    )
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.applicant.display_name + " applied to " + self.job.role
    

    class Meta:
        ordering = ['status', '-applied_on']
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

