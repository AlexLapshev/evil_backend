import pytest
from starlette.testclient import TestClient

from api.main import app

client = TestClient(app)

test_url = "/api/v1/playlist"


@pytest.mark.parametrize('id, status', [(2, 200), (100, 404), (8, 403)])
def test_get_playlist(client, id, status):
    response = client.get(test_url+"/get?id={}".format(id))
    assert response.status_code == status


@pytest.mark.parametrize('playlist_x_track, status', [({'playlist_id': 1, 'track_id': 5}, 201),
                                                      ({'playlist_id': 1, 'track_id': 5}, 409),
                                                      ({'playlist_id': 1, 'track': 5}, 422),
                                                      ({'playlist': 1, 'track_id': 5}, 422)
                                                      ])
def test_update_playlist(client, playlist_x_track, status):
    response = client.post(
        test_url+"/update/",
        headers={"Content-Type": "application/json"},
        json={"playlist_id": playlist_x_track.get('playlist_id'), "track_id": playlist_x_track.get('track_id')}
    )
    assert response.status_code == status


@pytest.mark.parametrize('playlist_x_track, status', [({'playlist_id': 1, 'track_id': 5}, 200),
                                                      ({'playlist_id': 1, 'track_id': 5}, 404),
                                                      ({'playlist_id': 1, 'track': 5}, 422),
                                                      ({'playlist': 1, 'track_id': 5}, 422)
                                                      ])
def test_delete_from_playlist(client, playlist_x_track, status):
    response = client.delete(
        test_url + "/update/",
        headers={"Content-Type": "application/json"},
        json={"playlist_id": playlist_x_track.get('playlist_id'), "track_id": playlist_x_track.get('track_id')}
    )
    assert response.status_code == status
