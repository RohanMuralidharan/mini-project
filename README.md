Personalized-content-based-music-recomendation-system-using-Spotify-API
A mini project to build a content based recommendation system using big data and machine learning with Apache Spark and Kafka.

https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks

Quick Setup
Create a Python virtual environment and activate it:

Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1
Install dependencies:

pip install -r requirements.txt
Create .env from .env.example and fill your Spotify credentials.

Common entry points:

spotify_api.py: utility functions to access Spotify API.
dashboard.py or Spotify Dashboard/spotify_viz.py: visualization/dashboard scripts.
producer.ipynb / consumer_kafka.ipynb: Kafka producer/consumer examples.
Run the dashboard (example):

python "Spotify Dashboard/spotify_viz.py"
If you want, I can: add a runnable wrapper script, run a quick dependency check, or open notebooks and extract runnable examples. Which would you like next?

Demo: fetch your saved tracks
Create .env from .env.example and fill your Spotify credentials.

Run the small demo script (this may open a browser to complete OAuth):

pip install -r requirements.txt
python fetch_demo.py
The demo writes saved_tracks_demo.csv in the current folder and prints a few tracks.
Notes:

If you prefer not to authenticate with your account, you can instead edit Spotify Dashboard/spotify_viz.py to point at a local CSV file and run the dashboard without OAuth.
I added spotify_client.py with helper functions to create a spotipy.Spotify client and fetch saved tracks as a DataFrame.
