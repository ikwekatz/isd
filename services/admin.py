# from django.contrib import admin
# from .models import (
#     SupportedSystem,
#     SupportService,
#     ExternalReporter,
#     SupportTicket,
#     StatisticType,
#     StatisticsRecord
# )
#
#
# @admin.register(SupportedSystem)
# class SupportedSystemAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)
#
#
# @admin.register(SupportService)
# class SupportServiceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)
#
#
# @admin.register(ExternalReporter)
# class ExternalReporterAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'email', 'phone_number')
#     search_fields = ('full_name', 'email', 'phone_number')
#
#
# @admin.register(SupportTicket)
# class SupportTicketAdmin(admin.ModelAdmin):
#     list_display = (
#         'reporter_name',
#         'user_type',
#         'system',
#         'service',
#         'status',
#         'submitted_at',
#         'resolved_at',
#         'resolved_by',
#     )
#     list_filter = ('user_type', 'status', 'system', 'service')
#     search_fields = (
#         'internal_user_name',
#         'external_user__full_name',
#         'description',
#         'system__name',
#         'service__name',
#     )
#     readonly_fields = ('submitted_at', 'resolved_at')
#     ordering = ('-submitted_at',)
#
#
# @admin.register(StatisticType)
# class StatisticTypeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name',)
#
#
# @admin.register(StatisticsRecord)
# class StatisticsRecordAdmin(admin.ModelAdmin):
#     list_display = (
#         'title',
#         'statistic_type',
#         'prepared_by',
#         'start_date',
#         'end_date',
#         'date_prepared'
#     )
#     list_filter = ('statistic_type', 'prepared_by', 'start_date', 'end_date')
#     search_fields = ('title', 'description')
#     readonly_fields = ('date_prepared',)


from django.contrib import admin
from .models import (
    SupportedSystem,
    SupportService,
    SupportTicket,
    StatisticType,
    StatisticsRecord, SubService,

)
from django import forms

@admin.register(SupportedSystem)
class SystemAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.add_supportedsystem')
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.change_supportedsystem')
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.delete_supportedsystem')


@admin.register(SupportService)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name']
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser  or request.user.has_perm('services.add_supportservice')
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  or request.user.has_perm('services.change_supportservice')
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  or request.user.has_perm('services.delete_supportservice')
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or  request.user.has_perm('services.view_supportservice')


@admin.register(StatisticType)
class StatisticTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff or request.user.has_perm('services.add_statistictype')
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff or request.user.has_perm('services.change_statistictype')
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff or request.user.has_perm('services.delete_statistictype')
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.view_statistictype')

@admin.register(StatisticsRecord)
class StatisticRecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'statistic_type', 'start_date', 'end_date', 'prepared_by']
    exclude = ['prepared_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.prepared_by = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.add_statisticsrecord')
    def has_add_permission(self, request, obj=None):
        return  request.user.has_perm('services.add_statisticsrecord')
    def has_change_permission(self, request, obj=None):
        return  request.user.has_perm('services.change_statisticsrecord')
    def has_view_permission(self, request, obj=None):
        return request.user.has_perm('services.view_statisticsrecord')


class SupportTicketAdminForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = '__all__'





@admin.register(SupportTicket)
class TicketAdmin(admin.ModelAdmin):
    form = SupportTicketAdminForm
    list_display = ['system', 'service', 'status', 'resolved_by', 'description']
    exclude = ['resolved_by']

    class Meta:
        widgets = {
            'service': forms.Select(attrs={'onchange': 'console.log("HTML ONCHANGE:", this.value)'}),
        }

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.resolved_by = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.delete_supportticket')

    def has_add_permission(self, request, obj=None):
        return request.user.has_perm('services.add_supportticket')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('services.change_supportticket')

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.has_perm('services.view_supportticket')
