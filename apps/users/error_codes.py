from django.db.models import TextChoices


class AccountErrorCodes(TextChoices):
    PASSWORD_MISMATCH = "Passwords do not match. Please try Again."
    USER_EXIST = "User already exists. Please try Again."
    UNKNOWN_USER = "Unable to find the user. Please try Again."
    INVALID_PASSWORD = "Given password is incorrect. Please try Again."
    INVALID_TOKEN = "Given password reset token is incorrect. Please try Again."
