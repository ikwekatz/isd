from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    department = models.ForeignKey('office.Department', null=True, blank=True, on_delete=models.SET_NULL)
    section = models.ForeignKey('office.Section', null=True, blank=True, on_delete=models.SET_NULL)
    unit = models.ForeignKey('office.Unit', null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


    def clean(self):
        super().clean()
        if self.unit and (self.department or self.section):
            raise ValidationError("User cannot belong to both a Unit and Department/Section at the same time.")
        if not self.unit and not (self.department and self.section):
            raise ValidationError("User must belong to either a Unit or both a Department and Section.")



class Role(Group):
    class Meta:
        proxy = True
        verbose_name = 'ROLE'
        verbose_name_plural = 'ROLES'
