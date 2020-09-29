import pytest


test_url = "/api/v1/artists/"


def test_get_all_artists(client):
    response = client.get(test_url)
    assert response.status_code == 200


@pytest.mark.parametrize('artist_id, status', [(1, 200), (100, 404)])
def test_get_one_artist(client, artist_id, status):
    response = client.get(test_url+str(artist_id))
    assert response.status_code == status


@pytest.mark.parametrize('artist_id, status', [(1, 200), (100, 404)])
def test_get_artist_releases(client, artist_id, status):
    response = client.get(test_url+str(artist_id))
    assert response.status_code == status


@pytest.mark.parametrize('artist_id, status', [(1, 200), (100, 404)])
def test_get_artist_tracks(client, artist_id, status):
    response = client.get(test_url+str(artist_id)+'/tracks')
    assert response.status_code == status
