from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database connection
engine = create_engine('postgresql://postgres:awssama69@localhost/spotify_trend')

# Load data and train model with deduplication
print("Loading data...")
df = pd.read_sql("""
    SELECT DISTINCT ON (t.track_id, t.track_name, a.artist_name)
        t.track_id, t.track_name, a.artist_name,
        f.danceability, f.energy, f.loudness, f.speechiness,
        f.acousticness, f.instrumentalness, f.liveness, f.valence, f.tempo,
        EXTRACT(YEAR FROM tm.full_date) AS year
    FROM dim_track t
    JOIN fact_music_features f ON t.track_id = f.track_id
    JOIN fact_track_popularity p ON t.track_id = p.track_id
    JOIN dim_artist a ON p.artist_id = a.artist_id
    JOIN dim_time tm ON p.time_id = tm.time_id
    ORDER BY t.track_id, t.track_name, a.artist_name, p.popularity DESC
""", engine)

print("Training model...")
features = df[['danceability', 'energy', 'loudness', 'speechiness',
               'acousticness', 'instrumentalness', 'liveness', 'valence']]
knn = NearestNeighbors(n_neighbors=11, metric='cosine').fit(features)


def get_unique_songs(song_list):
    """Helper function to remove duplicate songs based on track_id"""
    seen = set()
    unique_songs = []
    for song in song_list:
        identifier = (song['track_id'], song['track_name'], song['artist_name'])
        if identifier not in seen:
            seen.add(identifier)
            unique_songs.append(song)
    return unique_songs


# Routes
@app.route('/recommend', methods=['POST'])
def recommend():
    song_name = request.json.get('song_name', '').strip()
    if not song_name:
        return jsonify({"error": "Please provide a song name"}), 400

    # Find all matches (case insensitive) and get the most popular version
    matches = df[df['track_name'].str.contains(song_name, case=False, regex=False)]
    if matches.empty:
        return jsonify({"error": f"Song '{song_name}' not found"}), 404

    # Group by track name and artist, then get the most popular version
    best_matches = matches.sort_values(['track_name', 'artist_name', 'energy'],
                                       ascending=[True, True, False]) \
        .drop_duplicates(['track_name', 'artist_name'])

    # Get the first match (most relevant)
    input_song_idx = best_matches.index[0]
    song_features = features.loc[input_song_idx].values.reshape(1, -1)

    # Get recommendations and remove duplicates
    _, indices = knn.kneighbors(song_features)
    recommendations = df.iloc[indices[0][1:]].to_dict('records')
    unique_recommendations = get_unique_songs(recommendations)

    return jsonify({
        "input_song": df.iloc[input_song_idx][['track_name', 'artist_name']].to_dict(),
        "recommendations": unique_recommendations[:10]  # Return top 10 unique recommendations
    })


@app.route('/mood', methods=['POST'])
def mood_playlist():
    moods = {
        'party': {'energy': (0.8, 1), 'valence': (0.7, 1)},
        'chill': {'energy': (0, 0.4), 'acousticness': (0.7, 1)},
        'sad': {'valence': (0, 0.3), 'energy': (0, 0.5)},
        'focus': {'instrumentalness': (0.7, 1), 'speechiness': (0, 0.1)}
    }

    mood = request.json.get('mood', '').lower()
    if mood not in moods:
        return jsonify({"error": "Invalid mood"}), 400

    filtered = df.copy()
    for feature, (min_val, max_val) in moods[mood].items():
        filtered = filtered[filtered[feature].between(min_val, max_val)]

    # Get unique songs and sample from them
    unique_songs = filtered.drop_duplicates(['track_id', 'track_name', 'artist_name'])
    sample_size = min(20, len(unique_songs))
    return jsonify(unique_songs.sample(sample_size).to_dict('records'))


@app.route('/compare', methods=['POST'])
def compare_songs():
    song1 = request.json.get('song1', '').strip()
    song2 = request.json.get('song2', '').strip()

    if not song1 or not song2:
        return jsonify({"error": "Please provide two song names"}), 400

    # Find matches for each song (case insensitive)
    match1 = df[df['track_name'].str.contains(song1, case=False, regex=False)]
    match2 = df[df['track_name'].str.contains(song2, case=False, regex=False)]

    if len(match1) == 0 or len(match2) == 0:
        return jsonify({"error": "Could not find both songs"}), 404

    # Get the most popular version of each song
    song_a = match1.sort_values('energy', ascending=False).iloc[0].to_dict()
    song_b = match2.sort_values('energy', ascending=False).iloc[0].to_dict()

    return jsonify([song_a, song_b])


@app.route('/time-machine/<int:year>')
def time_machine(year):
    yearly_songs = df[df['year'] == year]
    if yearly_songs.empty:
        return jsonify({"error": f"No songs found for year {year}"}), 404

    # Get top 20 unique most energetic songs
    unique_songs = yearly_songs.drop_duplicates(['track_id', 'track_name', 'artist_name'])
    return jsonify(unique_songs.nlargest(20, 'energy').to_dict('records'))


@app.route('/artist', methods=['POST'])
def artist_songs():
    artist_name = request.json.get('artist_name', '').strip()
    if not artist_name:
        return jsonify({"error": "Please provide an artist name"}), 400

    # Case-insensitive search with exact matching preferred
    artist_pattern = f"%{artist_name}%"
    exact_match = df[df['artist_name'].str.lower() == artist_name.lower()]

    if not exact_match.empty:
        songs = exact_match
    else:
        songs = df[df['artist_name'].str.contains(artist_name, case=False)]

    if songs.empty:
        return jsonify({"error": f"Artist '{artist_name}' not found"}), 404

    # Get unique songs sorted by popularity (energy as proxy)
    unique_songs = songs.drop_duplicates(['track_id', 'track_name']) \
        .sort_values('energy', ascending=False)

    return jsonify({
        "artist": songs.iloc[0]['artist_name'],  # Get the correct artist name casing
        "songs": unique_songs.to_dict('records')
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)