from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

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
    budget_status = models.BooleanField(default=False, db_comment='False - Not Budgeted, True - Budgeted', )

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
            return f"{self.name}"
        elif self.section:
            return f"{self.name}"
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



class BudgetType(models.TextChoices):
    OGT = "Own Source"
    OC = "Other Charges"
    DEV = "Development Budget"
    OTHER = "Other"


class Budget(models.Model):
    financial_year = models.ForeignKey(
        FinancialYear,
        on_delete=models.PROTECT,
        related_name="budgets"
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="budgets"
    )
    budget_type = models.CharField(
        max_length=50,
        choices=BudgetType.choices
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("financial_year", "activity", "budget_type")
        verbose_name_plural = "Budgets"

    def __str__(self):
        return f"{self.activity} - {self.financial_year} ({self.budget_type}) : {self.amount}"



class Expenditure(models.Model):
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.PROTECT, related_name='expenditures')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='expenditures')
    budget_type = models.CharField(max_length=50, choices=BudgetType.choices, blank=True, null=True)
    expenditure_date = models.DateField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        budget = Budget.objects.filter(
            financial_year=self.financial_year,
            activity=self.activity,
            budget_type=self.budget_type
        ).first()
        if budget:
            total_expenditure = Expenditure.objects.filter(
                financial_year=self.financial_year,
                activity=self.activity,
                budget_type=self.budget_type
            ).exclude(pk=self.pk).aggregate(models.Sum('amount'))['amount__sum'] or 0

            if total_expenditure + self.amount > budget.amount:
                raise ValidationError(
                    f"Total expenditure ({total_expenditure + self.amount}) exceeds the budget ({budget.amount}) "
                    f"for activity {self.activity} and budget type {self.budget_type}."
                )
        else:
            raise ValidationError(f"No budget defined for activity {self.activity} and budget type {self.budget_type}.")

    def __str__(self):
        return f"{self.activity.name} - {self.budget_type} ({self.amount})"