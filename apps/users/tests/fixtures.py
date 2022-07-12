import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User, Roles


class ApiClient(APIClient):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", AnonymousUser())
        super().__init__(*args, **kwargs)
        self._user = None
        self.token = None
        self.user = user
        if not user.is_anonymous:
            self.token = str(RefreshToken.for_user(user).access_token)

    def _base_environ(self, **request):
        environ = super()._base_environ(**request)
        if not self.user.is_anonymous:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {self.token}"
        return environ


@pytest.fixture
def super_admin_user(db):
    """Return a Django super admin user."""
    return User.objects.create_superuser("superadmin@example.com", "password")


@pytest.fixture
def admin_user(db):
    """Return a admin user."""
    return User.objects.create_user(
        email="admin@example.com",
        username="admin@example.com",
        password="password",
        first_name="admin",
        is_staff=True,
        is_active=True,
        role=Roles.ADMIN,
    )


@pytest.fixture
def user(db):
    """Return a user."""
    return User.objects.create_user(
        email="user@example.com",
        username="user@example.com",
        password="password",
        first_name="user",
        is_staff=False,
        is_active=True,
        role=Roles.USER,
    )


@pytest.fixture
def admin_users(admin_user):
    """Return admin members."""
    admin_users = User.objects.bulk_create(
        [
            User(
                email="admin1_test@example.com",
                username="admin1_test@example.com",
                password="password",
                first_name="admin1",
                is_staff=True,
                is_active=True,
                role=Roles.ADMIN,
            ),
            User(
                email="admin2_test@example.com",
                username="admin2_test@example.com",
                password="password",
                first_name="admin2",
                is_staff=True,
                is_active=True,
                role=Roles.ADMIN,
            ),
        ]
    )
    return [admin_user] + admin_users


@pytest.fixture
def users(user):
    """Return users."""
    users = User.objects.bulk_create(
        [
            User(
                email="user1_test@example.com",
                username="user1_test@example.com",
                password="password",
                first_name="user1",
                is_staff=False,
                is_active=True,
            ),
            User(
                email="user2_test@example.com",
                username="user2_test@example.com",
                password="password",
                first_name="user2",
                is_staff=False,
                is_active=True,
            ),
        ]
    )
    return [user] + users


@pytest.fixture
def admin_api_client(admin_user):
    return ApiClient(user=admin_user)


@pytest.fixture
def superuser_api_client(superuser):
    return ApiClient(user=superuser)


@pytest.fixture
def user_api_client(user):
    return ApiClient(user=user)


@pytest.fixture
def api_client(db):
    return ApiClient(user=AnonymousUser())

