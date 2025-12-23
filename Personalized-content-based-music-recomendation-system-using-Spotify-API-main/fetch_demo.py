"""Small demo script that uses `spotify_client` to fetch saved tracks and save a CSV.

Run after creating a `.env` (or exporting environment variables).
"""
from dotenv import load_dotenv
import os
from spotify_client import get_spotify_client, get_saved_tracks_df


def main():
    load_dotenv()
    try:
        sp = get_spotify_client()
    except Exception as e:
        print('Error creating Spotify client:', e)
        print('Make sure you created a .env file (see .env.example) and filled credentials.')
        return

    print('Fetching saved tracks (may open a browser for OAuth)...')
    try:
        df = get_saved_tracks_df(sp, limit=50, max_tracks=200)
    except Exception as e:
        print('Error fetching tracks:', e)
        return

    if df.empty:
        print('No saved tracks returned.')
        return

    out = os.path.join(os.getcwd(), 'saved_tracks_demo.csv')
    df.to_csv(out, index=False)
    print(f'Saved {len(df)} tracks to', out)
    print(df[['name','artists']].head(10).to_string(index=False))


if __name__ == '__main__':
    main()
