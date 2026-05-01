from .models import JobStatus

def update_commission_status(commission):
    full_status = JobStatus.objects.get(name="FULL")
    open_status = JobStatus.objects.get(name="OPEN")

    jobs = commission.jobs.all()

    if jobs.exists() and all(job.status == full_status for job in jobs):
        commission.status = full_status
    else:
        commission.status = open_status

    commission.save(update_fields=["status"])