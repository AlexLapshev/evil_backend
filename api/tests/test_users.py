import pytest

from pathlib import Path

test_url = "/api/v1/users"


def test_user_info(client, access_token):
    response = client.get(
        test_url + '/me',
        headers={'Authorization': 'Bearer ' + access_token}
    )
    assert response.status_code == 200


@pytest.mark.parametrize('playlist_x_track, status', [({'playlist_id': 3, 'track_id': 25}, 201),
                                                      ({'playlist_id': 1, 'track_id': 4}, 403),
                                                      ({'playlist_id': 3, 'track': 25}, 422),
                                                      ({'playlist': 1, 'track_id': 5}, 422)
                                                      ])
def test_add_track_to_playlist(client, access_token, playlist_x_track, status):
    playlist_id = str(playlist_x_track.get('playlist_id'))
    track_id = str(playlist_x_track.get('track_id'))
    response = client.post(
        test_url + '/playlist/' + playlist_id + '?track_id=' + track_id,
        headers={
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + access_token
        },

    )
    assert response.status_code == status


@pytest.mark.parametrize('playlist_x_track, status', [({'playlist_id': 3, 'track_id': 1}, 200),
                                                      ({'playlist_id': 2, 'track_id': 1}, 403),
                                                      ({'playlist_id': 1, 'track': 4}, 422),
                                                      ({'playlist': 1, 'track_id': 4}, 422)
                                                      ])
def test_delete_track_from_playlist(client, access_token, playlist_x_track, status):
    playlist_id = str(playlist_x_track.get('playlist_id'))
    track_id = str(playlist_x_track.get('track_id'))
    response = client.delete(
        test_url + '/playlist/' + playlist_id + '?track_id=' + track_id,
        headers={
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + access_token
        },
    )
    assert response.status_code == status


@pytest.mark.parametrize('track_id, status', [(22, 201), (22, 409)])
def test_like_track(client, access_token, track_id, status):
    response = client.post(
        test_url + '/track/' + str(track_id) + '/like',
        headers={
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + access_token
        },
    )
    assert response.status_code == status


@pytest.mark.parametrize('track_id, status', [(12, 201), (12, 409)])
def test_unlike_track(client, access_token, track_id, status):
    response = client.delete(
        test_url + '/track/' + str(track_id) + '/like',
        headers={
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + access_token
        },
    )
    assert response.status_code == status


@pytest.mark.parametrize('artist_id, status', [(1, 201), (1, 409), (555, 404)])
def test_subscribe_artist(client, access_token, artist_id, status):
    response = client.post(
        test_url + '/artist/' + str(artist_id) + '/subscribe',
        headers={
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + access_token
        },
    )
    assert response.status_code == status


@pytest.mark.parametrize('artist_id, status', [(10, 201), (10, 409)])
def test_unsubscribe_artist(client, access_token, artist_id, status):
    response = client.delete(
        test_url + '/artist/' + str(artist_id) + '/subscribe',
        headers={
            "Content-Type": "application/json",
            'Authorization': 'Bearer ' + access_token
        },
    )
    assert response.status_code == status


@pytest.mark.parametrize('playlist_name, playlist_public, playlist_cover, status', [
    ("test", True, "test.png", 201),
    ("test", True, "test.pngg", 409),
])
def test_create_playlist(client, access_token, playlist_name, playlist_public, playlist_cover, status):
    path = Path(__file__).parent / playlist_cover
    with open(path, "rb") as image:
        response = client.post(
            test_url + '/playlists',
            headers={
                'Authorization': 'Bearer ' + access_token,
            },
            data={
                "playlist_name": playlist_name,
                "playlist_public": playlist_public,
                "playlist_cover": image
            }
        )
    assert response.status_code == status
