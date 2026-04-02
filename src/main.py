"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Stress-test profiles: expected, diverse, and adversarial/edge-case users.
    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "valence": 0.85,
            "tempo_bpm": 130,
            "likes_acoustic": False,
            "preferred_decade": 2010,
            "preferred_mood_tags": ["euphoric", "confident", "uplifting"],
            "target_popularity": 85,
            "likes_instrumental": False,
            "target_loudness_db": -6,
            "mode": "genre_first",
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "valence": 0.60,
            "tempo_bpm": 76,
            "likes_acoustic": True,
            "preferred_decade": 2020,
            "preferred_mood_tags": ["nostalgic", "calm", "introspective"],
            "target_popularity": 60,
            "likes_instrumental": True,
            "target_loudness_db": -14,
            "mode": "mood_first",
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "valence": 0.45,
            "tempo_bpm": 150,
            "likes_acoustic": False,
            "preferred_decade": 2000,
            "preferred_mood_tags": ["aggressive", "driving", "rebellious"],
            "target_popularity": 75,
            "likes_instrumental": False,
            "target_loudness_db": -5,
            "mode": "energy_focused",
        },
        "Conflict Case (High Energy + Melancholic)": {
            "genre": "lofi",
            "mood": "melancholic",
            "energy": 0.90,
            "valence": 0.20,
            "tempo_bpm": 84,
            "likes_acoustic": True,
            "preferred_decade": 1990,
            "preferred_mood_tags": ["melancholic", "nostalgic", "yearning"],
            "target_popularity": 55,
            "likes_instrumental": True,
            "target_loudness_db": -12,
            "mode": "mood_first",
        },
        "Out-of-Range Energy (1.20)": {
            "genre": "classical",
            "mood": "contemplative",
            "energy": 1.20,
            "valence": 0.50,
            "tempo_bpm": 62,
            "likes_acoustic": True,
            "preferred_decade": 1980,
            "preferred_mood_tags": ["contemplative", "serene", "meditative"],
            "target_popularity": 40,
            "likes_instrumental": True,
            "target_loudness_db": -18,
            "mode": "balanced",
        },
    }

    for profile_name, user_prefs in profiles.items():
        mode = user_prefs.get("mode", "balanced")
        recommendations = recommend_songs(
            user_prefs,
            songs,
            k=5,
            mode=mode,
            diversity_penalty=0.80,
        )

        print(f"\nProfile: {profile_name}")
        print(f"Scoring mode: {mode}")
        print("=" * 72)

        rows = []
        for rank, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            rows.append(
                [
                    rank,
                    song["title"],
                    song["artist"],
                    song["genre"],
                    f"{score:.2f}",
                    explanation,
                ]
            )

        headers = ["#", "Title", "Artist", "Genre", "Base Score", "Reasons"]
        if tabulate:
            print(tabulate(rows, headers=headers, tablefmt="grid", maxcolwidths=[None, 22, 18, 14, 10, 64]))
        else:
            print(" | ".join(headers))
            print("-" * 140)
            for row in rows:
                print(" | ".join(str(col) for col in row))
        print("-" * 72)


if __name__ == "__main__":
    main()
