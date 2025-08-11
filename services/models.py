from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from activities.models import Activity

User = get_user_model()


class SupportedSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SupportService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    activities = models.ForeignKey(Activity, on_delete=models.PROTECT, related_name='services', null=True)
    is_related_to_system = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SubService(models.Model):
    service = models.ForeignKey(SupportService, on_delete=models.CASCADE, related_name="sub_services")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.service.name} - {self.name}"

class ExternalReporter(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name


class SupportTicket(models.Model):
    USER_TYPE_CHOICES = (
        ('internal', 'Internal User (Staff)'),
        ('external', 'External'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    internal_user_name = models.CharField(max_length=100, blank=True, null=True)
    external_user = models.CharField(max_length=100, blank=True, null=True)
    system = models.ForeignKey(SupportedSystem, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(SupportService, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_tickets')

    def reporter_name(self):
        if self.user_type == 'internal' and self.internal_user_name:
            return self.internal_user_name
        elif self.external_user:
            return self.external_user
        return "NA"

    class Meta:
        verbose_name_plural = "Services Records"
        verbose_name = "Service Record"


class StatisticType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    activities = models.ForeignKey(Activity, on_delete=models.PROTECT, related_name='statistic_types', null=True)

    def __str__(self):
        return self.name


class StatisticsRecord(models.Model):
    title = models.CharField(max_length=255)
    statistic_type = models.ForeignKey(StatisticType, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    prepared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    date_prepared = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='statistics/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.statistic_type})"

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be earlier than start date.")
