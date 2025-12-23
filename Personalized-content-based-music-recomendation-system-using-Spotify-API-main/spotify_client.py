"""Lightweight Spotify client helpers used by the repo.

Functions here read credentials from environment variables:
  - `SPOTIFY_CLIENT_ID`
  - `SPOTIFY_CLIENT_SECRET`
  - `SPOTIFY_REDIRECT_URI`

Uses Spotipy's `SpotifyOAuth` to build an authenticated client.
"""
from typing import Dict
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_spotify_client(scope: str = 'user-library-read') -> spotipy.Spotify:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

    if not (client_id and client_secret and redirect_uri):
        raise EnvironmentError('Set SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and SPOTIFY_REDIRECT_URI in environment')

    auth_manager = SpotifyOAuth(client_id=client_id,
                                client_secret=client_secret,
                                redirect_uri=redirect_uri,
                                scope=scope)
    return spotipy.Spotify(auth_manager=auth_manager)


def _select_fields(track_response: Dict) -> Dict:
    return {
        'id': str(track_response['track']['id']),
        'name': str(track_response['track']['name']),
        'artists': [artist['name'] for artist in track_response['track']['artists']],
        'duration_ms': track_response['track']['duration_ms'],
        'popularity': track_response['track']['popularity'],
        'added_at': track_response['added_at']
    }


def get_saved_tracks_df(sp: spotipy.Spotify, limit: int = 50, max_tracks: int = None) -> pd.DataFrame:
    """Fetch user's saved tracks and enrich with audio features.

    Returns a pandas DataFrame similar to the original notebook's `tracks_df`.
    """
    saved = sp.current_user_saved_tracks(limit=limit)
    tracks = [_select_fields(t) for t in saved['items']]

    while saved['next']:
        saved = sp.next(saved)
        tracks.extend([_select_fields(t) for t in saved['items']])
        if max_tracks and len(tracks) >= max_tracks:
            tracks = tracks[:max_tracks]
            break

    df = pd.DataFrame(tracks)
    if df.empty:
        return df

    df['artists'] = df['artists'].apply(lambda artists: artists[0])
    df['duration_s'] = df['duration_ms'].apply(lambda d: d / 1000)

    # fetch audio features in batches
    ids = df['id'].tolist()
    audio_features = {}
    for track_id in ids:
        feat = sp.audio_features(track_id)[0]
        audio_features[track_id] = feat

    def get_feat(track_id, key, default=None):
        v = audio_features.get(track_id)
        return v.get(key) if v else default

    df['acousticness'] = df['id'].apply(lambda i: get_feat(i, 'acousticness'))
    df['danceability'] = df['id'].apply(lambda i: get_feat(i, 'danceability'))
    df['energy'] = df['id'].apply(lambda i: get_feat(i, 'energy'))
    df['instrumentalness'] = df['id'].apply(lambda i: get_feat(i, 'instrumentalness'))
    df['liveness'] = df['id'].apply(lambda i: get_feat(i, 'liveness'))
    df['speechiness'] = df['id'].apply(lambda i: get_feat(i, 'speechiness'))
    df['valence'] = df['id'].apply(lambda i: get_feat(i, 'valence'))
    df['tempo'] = df['id'].apply(lambda i: get_feat(i, 'tempo'))
    df['loudness'] = df['id'].apply(lambda i: get_feat(i, 'loudness'))

    return df


__all__ = [
    'get_spotify_client',
    'get_saved_tracks_df',
]
