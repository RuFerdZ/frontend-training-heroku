import json


def get_response_data(response):
    return json.loads(response.content.decode('utf-8'))


def assert_no_permission(response):
    content = get_response_data(response)
    assert "errors" in content, content
    assert "status" in content, content
    assert content["message"] == 'PermissionDenied'
    assert content["status"] == 'ERROR'
    assert content["errors"][0] == (
        "You do not have permission to perform this action."
    ), content["errors"]


def assert_unauthenticated(response):
    content = get_response_data(response)
    assert "errors" in content, content
    assert "status" in content, content
    assert content["message"] == 'NotAuthenticated'
    assert content["status"] == 'ERROR'
    assert content["errors"][0] == (
        "Authentication credentials were not provided."
    ), content["errors"]


def assert_validation_error(response):
    content = get_response_data(response)
    assert "errors" in content, content
    assert "status" in content, content
    assert content["message"] == 'ValidationError'
    assert content["status"] == 'ERROR'
    return content['errors']


def assert_not_found(response):
    content = get_response_data(response)
    assert "errors" in content, content
    assert "status" in content, content
    assert content["message"] == 'Http404'
    assert content["status"] == 'ERROR'
    assert content['errors'][0] == 'Not found.'

