"""Admin module of commissions project."""

from django.contrib import admin
from .models import CommissionType, Commission, JobStatus, ApplicationStatus, Job, JobApplication
# Register your models here.


class CommissionTypeAdmin(admin.ModelAdmin):
    model = CommissionType


class CommissionAdmin(admin.ModelAdmin):
    list_display = ('commission_type', 'maker', 'status', 'created_on')
    model = Commission


class JobStatusAdmin(admin.ModelAdmin):
    model = JobStatus


class ApplicationStatusAdmin(admin.ModelAdmin):
    model = ApplicationStatus


class JobAdmin(admin.ModelAdmin):
    list_display = ('commission', 'role', 'manpower_required', 'status')
    model = Job


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_on')
    model = JobApplication


admin.site.register(CommissionType, CommissionTypeAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)