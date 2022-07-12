from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

import uuid

from safedelete.models import SafeDeleteModel

from apps.common.email_templates import EmailTemplates
from apps.common.services import generate_token, send_mail


class Roles(models.TextChoices):
    # User Roles
    SUPER_ADMIN = 'SUPER_ADMIN', _('SUPER_ADMIN')
    ADMIN = 'ADMIN', _('ADMIN')
    USER = 'USER', _('USER')


class Company(SafeDeleteModel):
    name = models.BinaryField(max_length=100, null=True, blank=True)
    logo = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE,
                              related_name='managing_company', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class User(AbstractUser, SafeDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_super_admin(self):
        return self.role == Roles.SUPER_ADMIN or self.is_superuser

    def is_admin_user(self):
        return self.role in [Roles.ADMIN, Roles.SUPER_ADMIN]

    def is_user(self):
        return self.role == Roles.USER

    def generate_email_verification_code(self):
        verification = self.email_verifications.create(code=generate_token(6))
        send_mail(
            'Please confirm your email.',
            self.email,
            EmailTemplates.AUTH_VERIFICATION,
            {'verification_code': verification.code}
        )


class UserEmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='email_verifications'
    )
    code = models.PositiveIntegerField(max_length=6)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
