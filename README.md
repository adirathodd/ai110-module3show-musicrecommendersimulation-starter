# Music Recommender Simulation

## Project Summary

This project implements a modular music recommender that supports advanced feature scoring, multiple ranking strategies, diversity-aware reranking, and explainable recommendation output.

Key upgrades in this version:

- Added advanced song metadata beyond baseline fields.
- Implemented multiple scoring modes with strategy-style weight profiles.
- Added diversity penalties to reduce repeated artists/genres in top-k.
- Improved CLI readability using a formatted table that includes scoring reasons.

## Challenge Coverage

### Challenge 1: Advanced Song Features

The dataset in data/songs.csv now includes these additional attributes:

- popularity (0-100)
- release_decade
- mood_tags (pipe-delimited string, for example: nostalgic|calm|introspective)
- instrumentalness
- loudness_db
- live_performance

These are parsed and used by scoring logic in src/recommender.py.

### Challenge 2: Multiple Scoring Modes

The recommender supports these strategy modes:

- balanced
- genre_first
- mood_first
- energy_focused

Each mode uses a different weight profile for component scores, allowing users to switch ranking priorities without rewriting core logic.

### Challenge 3: Diversity and Fairness Logic

Top-k recommendations are selected via diversity-aware reranking:

- Artist repetition penalty: subtracts score when an artist already appears in selected results.
- Genre repetition penalty: subtracts score when a genre is overrepresented.

This helps avoid lists dominated by one artist or one genre.

### Challenge 4: Visual Summary Table

CLI output is now tabular in src/main.py:

- Uses tabulate for pretty grid output when available.
- Falls back to ASCII formatting if tabulate is missing.
- Includes rank, title, artist, genre, base score, and explanation reasons.

## How The System Works

1. Load songs from data/songs.csv.
2. Select a user profile and mode (for example genre_first).
3. Compute weighted component scores for every song.
4. Rerank with diversity penalties while building top-k.
5. Print recommendations as a table with detailed reasons.

## Scoring Logic

### Component Formula Style

For each component, similarity or match is converted into a 0..1 value and multiplied by the mode weight.

Examples:

- Genre match: exact match gives 1, else 0.
- Mood match: exact match gives 1, else 0.
- Energy similarity:

```text
energy_similarity = clamp(1 - abs(song_energy - user_energy), 0, 1)
energy_points = energy_similarity * weight_energy
```

- Popularity similarity:

```text
popularity_similarity = clamp(1 - abs(song_popularity - target_popularity) / 100, 0, 1)
```

- Decade similarity:

```text
decade_similarity = clamp(1 - abs(song_decade - preferred_decade) / 40, 0, 1)
```

- Mood-tag overlap:

```text
mood_tag_overlap = |user_tags INTERSECT song_tags| / |user_tags|
```

- Instrumental preference:
  - If user likes instrumental: use song instrumentalness directly.
  - If user dislikes instrumental: use (1 - instrumentalness).
  - If unspecified: neutral 0.5.

- Loudness alignment:

```text
loudness_alignment = clamp(1 - abs(song_loudness_db - target_loudness_db) / 30, 0, 1)
```

Total base score is the sum of all weighted components.

### Diversity Penalty Formula

When selecting each next recommendation:

```text
adjusted_score = base_score
                 - (diversity_penalty * artist_count[song.artist])
                 - (diversity_penalty * 0.6 * genre_count[song.genre])
```

This is applied iteratively while building top-k.

## Features Used

### Song Features

- id
- title
- artist
- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness
- popularity
- release_decade
- mood_tags
- instrumentalness
- loudness_db
- live_performance

### User Preference Fields

- genre
- mood
- energy
- likes_acoustic
- preferred_decade
- preferred_mood_tags
- target_popularity
- likes_instrumental
- target_loudness_db
- mode

## Setup and Run

1. Create a virtual environment (optional):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the CLI simulation:

```bash
python -m src.main
```

4. Run tests:

```bash
pytest
```

## Notes on Explainability

Every recommendation includes detailed reasons such as:

- component contribution per feature group
- selected mode
- artist diversity penalty
- genre diversity penalty
- final adjusted score

## Current Limitations

- The catalog is still small (30 songs), so behavior can be sensitive to individual rows.
- Mood tags are manually authored and simplified.
- No collaborative filtering or user history is used.
- Scoring weights are hand-tuned and not learned from feedback.

## Future Improvements

- Add user feedback loops to tune weights automatically.
- Add stronger fairness controls (for example per-genre caps in top-k).
- Introduce richer text/embedding features for lyrical or semantic similarity.
- Expand dataset size for better generalization.

