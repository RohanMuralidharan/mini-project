from pathlib import Path
import os
import subprocess
from dotenv import load_dotenv


def main():
    load_dotenv()

    # Ensure Spotipy env vars are available to scripts
    for env_key in ("SPOTIFY_CLIENT_ID", "SPOTIFY_CLIENT_SECRET", "SPOTIFY_REDIRECT_URI"):
        val = os.getenv(env_key)
        if val:
            os.environ.setdefault(env_key.replace('SPOTIFY_', 'SPOTIPY_') if env_key != 'SPOTIFY_REDIRECT_URI' else 'SPOTIPY_REDIRECT_URI', val)

    root = Path(__file__).parent
    candidates = [root / "Spotify Dashboard" / "spotify_viz.py", root / "dashboard.py"]
    target = None
    for c in candidates:
        if c.exists():
            target = c
            break

    if target is None:
        print("No dashboard script found. Please run one of the scripts in the repository manually.")
        return

    print(f"Launching Streamlit dashboard: {target}")
    try:
        subprocess.run(["streamlit", "run", str(target)], check=True)
    except FileNotFoundError:
        print("Streamlit is not installed or not on PATH. Install dependencies with: pip install -r requirements.txt")
    except subprocess.CalledProcessError as e:
        print("Streamlit exited with an error:", e)


if __name__ == '__main__':
    main()
