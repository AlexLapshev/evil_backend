import pytest

test_url = "/api/v1/"


@pytest.mark.parametrize('login_info, status', [({'login': 'failed_user', 'password': 'secret'}, 401),
                                                ({'login': 'johndoe', 'password': 'secret'}, 200)])
def test_user_login(client, login_info, status):
    response = client.post(
        test_url + 'token',
        data={'username': login_info.get('login'), 'password': login_info.get('password')}
    )
    assert response.status_code == status


def test_refresh_token(client, access_token):
    r = client.post(
        '/api/v1/token',
        data={'username': 'johndoe', 'password': 'secret'}
    )
    refresh_token = r.json().get('refresh_token')
    response = client.post(
        test_url + 'refresh-token',
        headers={
            "refresh_token": refresh_token
        }
    )
    assert response.status_code == 200
