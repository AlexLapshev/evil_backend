import pytest


test_url = "/api/v1/tracks/"


@pytest.mark.parametrize('track_id, status', [(1, 200), (100, 404)])
def test_track(client, track_id, status):
    response = client.get(test_url+str(track_id))
    assert response.status_code == status


def test_popular_tracks(client):
    response = client.get(test_url)
    assert response.status_code == 200
