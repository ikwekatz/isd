from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from authentication.models import CustomUser, Role
from office.models import Section, Department, Unit


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.none(), required=False)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'department', 'section', 'unit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially, no sections until department is selected
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['section'].queryset = Section.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department:
            self.fields['section'].queryset = Section.objects.filter(department=self.instance.department)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get('unit')
        department = cleaned_data.get('department')
        section = cleaned_data.get('section')

        if unit and (department or section):
            raise ValidationError("User cannot belong to both a Unit and Department/Section.")
        if not unit and not (department and section):
            raise ValidationError("User must belong to either a Unit or both a Department and Section.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # assign department, section, and unit fields
        user.department = self.cleaned_data.get('department')
        user.section = self.cleaned_data.get('section')
        user.unit = self.cleaned_data.get('unit')
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.none(), required=False)
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password', 'is_active', 'is_staff', 'department', 'section', 'unit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.department:
            self.fields['section'].queryset = Section.objects.filter(department=self.instance.department)
        else:
            self.fields['section'].queryset = Section.objects.none()

    def clean_password(self):
        return self.initial["password"]

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get('unit')
        department = cleaned_data.get('department')
        section = cleaned_data.get('section')

        if unit and (department or section):
            raise ValidationError("User cannot belong to both a Unit and Department/Section.")
        if not unit and not (department and section):
            raise ValidationError("User must belong to either a Unit or both a Department and Section.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.department = self.cleaned_data.get('department')
        user.section = self.cleaned_data.get('section')
        user.unit = self.cleaned_data.get('unit')
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'full_name', 'is_active', 'date_joined', 'department', 'section', 'unit')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'department', 'section', 'unit')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('full_name', 'department', 'section', 'unit')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'full_name', 'password1', 'password2',
                'department', 'section', 'unit',
                'is_active', 'is_staff'
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)

admin.site.register(Role, GroupAdmin)
