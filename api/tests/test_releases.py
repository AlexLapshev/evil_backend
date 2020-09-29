import pytest


test_url = "/api/v1/stream/releases/"


@pytest.mark.parametrize('release_id, status', [(1, 200), (666, 404)])
def test_release(client, release_id, status):
    response = client.get(test_url + '{}'.format(release_id))
    assert response.status_code == status


def test_all_releases(client):
    response = client.get(test_url)
    assert response.status_code == 200