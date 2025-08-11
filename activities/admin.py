from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError, PermissionDenied
from .models import FinancialYear, Activity
from django.utils.translation import gettext_lazy as _

class FinancialYearForm(forms.ModelForm):
    class Meta:
        model = FinancialYear
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if not start or not end:
            return cleaned_data
        if not (start.month == 7 and start.day == 1):
            raise ValidationError('Start date must be July 1.')

        expected_end_year = start.year + 1
        if not (end.month == 6 and end.day == 30 and end.year == expected_end_year):
            raise ValidationError('End date must be June 30 of the year after the start date.')

        return cleaned_data


@admin.register(FinancialYear)
class FinancialYearAdmin(admin.ModelAdmin):
    form = FinancialYearForm
    list_display = ('__str__', 'start_date', 'end_date')


class ActivityAdminForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and not self.user.has_perm('services.view_all_activities'):
            self.fields['unit'].widget = forms.HiddenInput()
            self.fields['section'].widget = forms.HiddenInput()

            # Pre-fill based on user's profile
            if hasattr(self.user, 'unit') and self.user.unit:
                self.initial['unit'] = self.user.unit
            elif hasattr(self.user, 'section') and self.user.section:
                self.initial['section'] = self.user.section

    def clean(self):
        cleaned_data = super().clean()

        # For admin users, validate their manual selection
        if self.user.has_perm('services.view_all_activities'):
            unit = cleaned_data.get('unit')
            section = cleaned_data.get('section')

            if unit and section:
                raise forms.ValidationError("Activity cannot belong to both a Unit and a Section.")
            if not unit and not section:
                raise forms.ValidationError("Activity must belong to either a Unit or a Section.")

        return cleaned_data

# @admin.register(Activity)
# class ActivityAdmin(admin.ModelAdmin):
#     form = ActivityAdminForm
#     list_display = ('name', 'description', 'financial_year', 'assigned_to')
#     list_filter = ('financial_year', 'name')
#     search_fields = ['name', 'description']
#
#     class ActivityAdmin(admin.ModelAdmin):
#         form = ActivityAdminForm
#
#     def get_form(self, request, obj=None, **kwargs):
#         Form = super().get_form(request, obj, **kwargs)
#         class RequestUserForm(Form):
#             def __new__(cls, *args, **kwargs):
#                 kwargs['user'] = request.user
#                 return Form(*args, **kwargs)
#
#         return RequestUserForm
#
#     def save_model(self, request, obj, form, change):
#         if not request.user.has_perm('services.view_all_activities'):
#             if hasattr(request.user, 'unit'):
#                 obj.unit = request.user.unit
#                 obj.section = None
#             elif hasattr(request.user, 'section'):
#                 obj.section = request.user.section
#                 obj.unit = None
#
#         super().save_model(request, obj, form, change)
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.has_perm('services.view_all_activities'):
#             return qs
#         if hasattr(request.user, 'unit'):
#             return qs.filter(unit=request.user.unit)
#         if hasattr(request.user, 'section'):
#             return qs.filter(section=request.user.section)
#         return qs.none()


class FinancialYearListFilter(admin.SimpleListFilter):
    title = _('Financial year')
    parameter_name = 'financial_year'

    def lookups(self, request, model_admin):
        return [(fy.id, str(fy)) for fy in FinancialYear.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(financial_year_id=self.value())
        return queryset


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    list_display = ('name', 'description', 'financial_year', 'assigned_to')
    list_filter = [FinancialYearListFilter]
    search_fields = ['name', 'description']

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)
        class RequestUserForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs['user'] = request.user
                return Form(*args, **kwargs)
        return RequestUserForm

    def save_model(self, request, obj, form, change):
        if not request.user.has_perm('services.view_all_activities'):
            if hasattr(request.user, 'unit'):
                obj.unit = request.user.unit
                obj.section = None
            elif hasattr(request.user, 'section'):
                obj.section = request.user.section
                obj.unit = None
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.has_perm('services.view_all_activities'):
            return qs
        if hasattr(request.user, 'unit'):
            return qs.filter(unit=request.user.unit)
        if hasattr(request.user, 'section'):
            return qs.filter(section=request.user.section)
        return qs.none()