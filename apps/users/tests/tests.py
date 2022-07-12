from django.conf import settings
from django.urls import reverse

from apps.common.tests.utils import get_response_data, assert_no_permission, assert_validation_error
from apps.users.error_codes import AccountErrorCodes


def test_user_self_join(api_client):
    data = {
        'email': 'user@example.com',
        'password': 'Password',
        'confirm_password': 'Password',
        'first_name': 'First',
        'last_name': 'Last'
    }
    url = reverse('auth-register')
    response = api_client.post(url, data)

    if settings.SELF_REGISTER:
        content = get_response_data(response)
        assert response.status_code == 201
        assert content['data']['id']
        assert content['data']['first_name'] == data['first_name']
        assert content['data']['last_name'] == data['last_name']
        assert content['data']['email'] == data['email']
    else:
        assert_no_permission(response)


def test_user_self_join_with_invalid_data(api_client):
    data = {
        'email': 'user@example',
        'password': 'Password123',
        'confirm_password': 'Password',
        'first_name': 'First',
        'last_name': 'Last'
    }
    url = reverse('auth-register')
    response = api_client.post(url, data)
    errors = assert_validation_error(response)
    assert errors[0]['email'][0] == 'Enter a valid email address.'
    assert errors[0]['confirm_password'][0] == AccountErrorCodes.PASSWORD_MISMATCH

