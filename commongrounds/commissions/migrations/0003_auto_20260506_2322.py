from django.db import migrations

def create_application_statuses(apps, schema_editor):
    ApplicationStatus = apps.get_model('commissions', 'ApplicationStatus')

    statuses = [
        ("PENDING", 1),
        ("ACCEPTED", 2),
        ("REJECTED", 3),
    ]

    for name, order in statuses:
        ApplicationStatus.objects.update_or_create(
            name=name,
            defaults={"order": order}
        )

def delete_application_statuses(apps, schema_editor):
    ApplicationStatus = apps.get_model('commissions', 'ApplicationStatus')
    ApplicationStatus.objects.filter(
        name__in=["PENDING", "ACCEPTED", "REJECTED"]
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0002_auto_20260506_2318'),
    ]

    operations = [
        migrations.RunPython(create_application_statuses, delete_application_statuses),
    ]
