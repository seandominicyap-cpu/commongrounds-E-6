from django.db import transaction
from django.db.models import Sum

from .models import (
    Commission,
    Job,
    JobApplication,
    JobStatus,
    ApplicationStatus
)


class CommissionService:

    @staticmethod
    def create_commission(author, data, jobs_data):
        """
        Creates a Commission and its Jobs atomically.
        """
        with transaction.atomic():
            commission = Commission.objects.create(
                maker=author,
                **data
            )

            for job_data in jobs_data:
                Job.objects.create(
                    commission=commission,
                    **job_data
                )

            return commission

    @staticmethod
    def apply_to_job(applicant, job):
        """
        Apply to a job with validation:
        - cannot apply twice
        - cannot apply if job is full
        """
        # ❌ Already applied
        if JobApplication.objects.filter(
            job=job,
            applicant=applicant
        ).exists():
            raise ValueError("Already applied to this job")

        accepted_status = ApplicationStatus.objects.get(name="ACCEPTED")

        accepted_count = JobApplication.objects.filter(
            job=job,
            status=accepted_status
        ).count()

        # ❌ Job is full
        if accepted_count >= job.manpower_required:
            raise ValueError("Job is already full")

        pending_status = ApplicationStatus.objects.get(name="PENDING")

        return JobApplication.objects.create(
            job=job,
            applicant=applicant,
            status=pending_status
        )

    @staticmethod
    def sync_commission_status(commission):
        """
        If ALL jobs are FULL → Commission becomes FULL
        Otherwise → OPEN
        """
        full_status = JobStatus.objects.get(name="FULL")
        open_status = JobStatus.objects.get(name="OPEN")

        jobs = commission.jobs.all()

        if jobs.exists() and all(job.status == full_status for job in jobs):
            commission.status = full_status
        else:
            commission.status = open_status

        commission.save(update_fields=["status"])

    @staticmethod
    def get_commission_summary(commission):
        """
        Returns:
        - total_manpower
        - open_manpower
        """
        total_manpower = (
            commission.jobs.aggregate(
                total=Sum("manpower_required")
            )["total"] or 0
        )

        accepted_status = ApplicationStatus.objects.get(name="ACCEPTED")

        accepted_count = JobApplication.objects.filter(
            job__commission=commission,
            status=accepted_status
        ).count()

        return {
            "total_manpower": total_manpower,
            "open_manpower": total_manpower - accepted_count
        }

def update_commission_status(commission):
    full_status = JobStatus.objects.get(name="FULL")
    open_status = JobStatus.objects.get(name="OPEN")

    jobs = commission.jobs.all()

    if jobs.exists() and all(job.status == full_status for job in jobs):
        commission.status = full_status
    else:
        commission.status = open_status

    commission.save(update_fields=["status"])