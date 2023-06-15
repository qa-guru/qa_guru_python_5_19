import requests
from jsonschema.validators import validate

from helper import load_json_schema, CustomSession, reqres_session


def test_requested_page_number():
    page = 2

    response = reqres_session.get('/api/users', params={'page': page})

    assert response.status_code == 200
    assert response.json()['page'] == page


def test_users_list_default_length():
    default_users_count = 6

    response = reqres_session.get('/api/users')

    assert len(response.json()['data']) == default_users_count


def test_single_user_not_found():
    response = requests.get('https://reqres.in/api/users/23')

    assert response.status_code == 404
    assert response.text == '{}'


def test_create_user():
    name = "jane"
    job = "job"

    response = requests.post(
        url='https://reqres.in/api/users',
        json={
            "name": name,
            "job": job}
    )

    assert response.status_code == 201
    assert response.json()['name'] == name


def test_create_user_schema_validation():
    name = "jane"
    job = "job"
    schema = load_json_schema('post_create_user.json')

    response = requests.post(
        url='https://reqres.in/api/users',
        json={
            "name": name,
            "job": job}
    )

    validate(instance=response.json(), schema=schema)


def test_delete_user_returns_204():
    response = requests.delete(url='https://reqres.in/api/users/2')

    assert response.status_code == 204
    assert response.text == ''
