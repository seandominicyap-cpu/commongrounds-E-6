"""Models of commmissions app."""

from django.db import models
from accounts.models import Profile
# Create your models here.


class CommissionType(models.Model):
    """Model that represents commission type."""

    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        """Class that provides ordering of commission types."""

        ordering = ["name"]


class Commission(models.Model):
    """Model that represents commissions."""
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('FULL', 'Full'),
    ]

    title = models.CharField(max_length=255)
    commission_type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions",
    )
    description = models.TextField()
    people_required = models.IntegerField()
    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'OPEN'
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """Class that provides ordering of commissions."""

        ordering = ["created_on"]
