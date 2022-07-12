from django.db.models import TextChoices


class EmailTemplates(TextChoices):
    AUTH_INVITATION = "auth/invitation{}"
    AUTH_VERIFICATION = "auth/verification{}"
    AUTH_LOGIN_2FA = "auth/login-2fa{}"
    AUTH_PASSWORD_RESET_REQUEST = "auth/request-reset-password{}"
    AUTH_VERIFY_AND_JOIN_PROJECT = "auth/verify-and-join-project{}"

    PROJECTS_USER_INVITATION = "projects/verify-and-join-project{}"
