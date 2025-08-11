from django.contrib import admin
from .models import Department, Section, Unit

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')
    search_fields = ('name','short_name')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'short_name')
    search_fields = ('name','department', 'short_name')
    list_filter = ('department','short_name')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name','short_name')
    search_fields = ('name','short_name')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Unit, UnitAdmin)