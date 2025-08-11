from django.core.exceptions import ValidationError
from django.db import models

from office.models import Unit, Section


class FinancialYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name_plural = "Financial Years"

    def __str__(self):
        return f"{self.start_date.year}/{self.end_date.year}"


class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    unit = models.ForeignKey(Unit, null=True, blank=True, related_name='activities', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, blank=True, related_name='activities', on_delete=models.CASCADE)
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='activities')

    date_performed = models.DateField(auto_now_add=True)

    def clean(self):
        super().clean()
        if not (hasattr(self, '_prefilled_unit_section') and self._prefilled_unit_section):
            if self.unit and self.section:
                raise ValidationError("Activity cannot belong to both a Unit and a Section.")
            if not self.unit and not self.section:
                raise ValidationError("Activity must belong to either a Unit or a Section.")

    def __str__(self):
        if self.unit:
            return f"{self.name} (Unit: {self.unit.name})"
        elif self.section:
            return f"{self.name} (Section: {self.section.name})"
        else:
            return self.name

    def assigned_to(self):
        return self.unit if self.unit else self.section
    assigned_to.short_description = 'Belongs To'
    class Meta:
        permissions = [
            ("view_all_activities", "Can view all activities regardless of unit or section"),
            ("view_department_activities", "Can view Department Activities "),
            ("view_unit_activities", "Can view Unit Activities "),
            ("view_section_activities", "Can view Section Activities "),
        ]
        verbose_name_plural = "Activities"
        verbose_name = "Activity"
